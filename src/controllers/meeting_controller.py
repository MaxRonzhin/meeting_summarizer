"""
Контроллер управления встречей.

Координирует процесс транскрибирования, обработки
и генерации саммари встречи.
"""

from datetime import datetime
import os
from typing import List
from src.services.audio_capture import AudioCaptureService
from src.services.stt_service import STTService
from src.services.summary_service import SummaryService
from src.services.transcript_processor import TranscriptProcessor
from src.models.transcript import TranscriptSegment, MeetingTranscript
from src.observers.transcript_observer import TranscriptObserver
from src.utils.logger import get_logger

logger = get_logger(__name__)

class MeetingController:
    """
    Контроллер управления процессом встречи.
    
    Координирует все этапы обработки встречи:
    захват аудио, транскрибирование, обработка
    и генерация саммари.
    """
    
    def __init__(
        self,
        audio_service: AudioCaptureService,
        stt_service: STTService,
        summary_service: SummaryService,
        transcript_processor: TranscriptProcessor
    ):
        """
        Инициализирует контроллер встречи.
        
        Args:
            audio_service: Сервис захвата аудио
            stt_service: Сервис транскрибирования
            summary_service: Сервис генерации саммари
            transcript_processor: Процессор транскрипции
        """
        self.audio_service = audio_service
        self.stt_service = stt_service
        self.summary_service = summary_service
        self.transcript_processor = transcript_processor
        self.observers: List[TranscriptObserver] = []
        self.segments: List[TranscriptSegment] = []
        self.is_meeting_active = False
        self.start_time = None
        logger.info("MeetingController инициализирован")
        
    def add_observer(self, observer: TranscriptObserver):
        """
        Добавляет наблюдателя за транскрипцией.
        
        Args:
            observer: Наблюдатель для уведомления о новых сегментах
        """
        self.observers.append(observer)
        
    def start_meeting(self):
        """
        Начинает встречу и процесс транскрибирования.
        
        Захватывает аудио, транскрибирует в реальном времени
        и уведомляет наблюдателей о новых сегментах.
        """
        logger.info("Начало встречи")
        self.is_meeting_active = True
        self.segments = []
        self.start_time = datetime.now()
        
        try:
            # Захват аудио
            audio_stream = self.audio_service.start_capture()
            
            # Транскрибирование в реальном времени
            for segment in self.stt_service.transcribe_stream(audio_stream):
                segment.start_time = (datetime.now() - self.start_time).total_seconds()
                self.segments.append(segment)
                
                # Уведомляем наблюдателей
                for observer in self.observers:
                    observer.on_new_segment(segment)
                    
        except KeyboardInterrupt:
            logger.info("Встреча прервана пользователем")
        except Exception as e:
            logger.error(f"Ошибка во время встречи: {e}")
        finally:
            self.stop_meeting()
    
    def stop_meeting(self):
        """
        Завершает встречу и генерирует саммари.
        
        Обрабатывает транскрипцию, генерирует саммари
        и сохраняет результаты в файлы.
        
        Returns:
            tuple: (summary, transcript_path, summary_path) - сгенерированное саммари и пути к файлам
        """
        logger.info("Завершение встречи")
        self.is_meeting_active = False
        self.audio_service.stop_capture()
        
        if self.segments:
            # Обработка транскрипции
            processed_segments = self.transcript_processor.process_segments(self.segments)
            
            # Создание объекта транскрипции
            transcript = MeetingTranscript(
                segments=processed_segments,
                created_at=self.start_time,
                duration=(datetime.now() - self.start_time).total_seconds()
            )
            
            # Сохранение транскрипции
            transcript_path = self.save_transcript(transcript)
            
            # Генерация саммари
            full_text = transcript.get_full_text()
            summary = self.summary_service.summarize(full_text)
            
            # Сохранение саммари
            summary_path = self.save_summary(summary, self.start_time)
            
            # Вывод в консоль
            logger.info("=== САММАРИ ВСТРЕЧИ ===")
            print(summary)
            logger.info("========================")
            logger.info(f"💾 Транскрипция сохранена в: {transcript_path}")
            logger.info(f"💾 Саммари сохранено в: {summary_path}")
            
            return summary, transcript_path, summary_path
        else:
            logger.warning("Нет данных для саммари")
            message = "Встреча не содержала речи"
            summary_path = self.save_summary(message, datetime.now())
            return message, None, summary_path
    
    def save_transcript(self, transcript: MeetingTranscript) -> str:
        """
        Сохраняет транскрипцию в файл.
        
        Args:
            transcript: Объект транскрипции для сохранения
            
        Returns:
            str: Путь к сохраненному файлу
        """
        # Создаем папку для результатов
        results_dir = "results"
        os.makedirs(results_dir, exist_ok=True)
        
        # Формируем имя файла
        timestamp = transcript.created_at.strftime("%Y%m%d_%H%M%S")
        filename = f"transcript_{timestamp}.txt"
        filepath = os.path.join(results_dir, filename)
        
        # Сохраняем транскрипцию
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"Транскрипция встречи от {transcript.created_at}\n")
            f.write(f"Длительность: {transcript.duration:.2f} секунд\n")
            f.write("=" * 50 + "\n\n")
            
            for segment in transcript.segments:
                speaker = segment.speaker or "Неизвестный"
                f.write(f"[{segment.start_time:.2f}s] {speaker}: {segment.text}\n")
        
        logger.info(f"Транскрипция сохранена в: {filepath}")
        return filepath
    
    def save_summary(self, summary: str, created_at: datetime) -> str:
        """
        Сохраняет саммари в файл.
        
        Args:
            summary: Текст саммари для сохранения
            created_at: Время создания саммари
            
        Returns:
            str: Путь к сохраненному файлу
        """
        # Создаем папку для результатов
        results_dir = "results"
        os.makedirs(results_dir, exist_ok=True)
        
        # Формируем имя файла
        timestamp = created_at.strftime("%Y%m%d_%H%M%S")
        filename = f"summary_{timestamp}.txt"
        filepath = os.path.join(results_dir, filename)
        
        # Сохраняем саммари
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"Саммари встречи от {created_at}\n")
            f.write("=" * 30 + "\n\n")
            f.write(summary)
            f.write("\n")
        
        logger.info(f"Саммари сохранено в: {filepath}")
        return filepath
