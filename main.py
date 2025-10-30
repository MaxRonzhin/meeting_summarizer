#!/usr/bin/env python3
"""
Главный файл запуска Meeting Summarizer.

Этот файл предоставляет основную точку входа в приложение,
автоматически настраивает модели и запускает процесс
транскрибирования и генерации саммари видеоконференций.
"""

from src.services.audio_capture import AudioCaptureService
from src.services.stt_service import WhisperSTTService
from src.services.summary_service import LlamaSummaryService
from src.services.transcript_processor import TranscriptProcessor
from src.controllers.meeting_controller import MeetingController
from src.observers.transcript_observer import ConsoleTranscriptObserver
from src.utils.logger import get_logger
from src.utils.model_downloader import setup_models
import sys

logger = get_logger(__name__)

def main():
    """
    Основная точка входа в приложение.
    
    Выполняет следующие шаги:
    1. Автоматическая настройка моделей (загрузка при необходимости)
    2. Инициализация всех сервисов
    3. Запуск процесса транскрибирования
    4. Генерация саммари по завершении
    """
    logger.info("Запуск Meeting Summarizer")
    
    try:
        # Автоматическая загрузка моделей
        whisper_model, llm_model_path = setup_models()
        
        # Инициализация сервисов
        audio_service = AudioCaptureService()
        stt_service = WhisperSTTService(whisper_model)
        summary_service = LlamaSummaryService(llm_model_path)
        transcript_processor = TranscriptProcessor()
        
        # Инициализация контроллера
        controller = MeetingController(
            audio_service=audio_service,
            stt_service=stt_service,
            summary_service=summary_service,
            transcript_processor=transcript_processor
        )
        
        # Добавляем наблюдателя для вывода транскрипции в консоль
        controller.add_observer(ConsoleTranscriptObserver())
        
        # Начинаем встречу
        try:
            logger.info("Нажмите Ctrl+C для завершения встречи")
            controller.start_meeting()
        except KeyboardInterrupt:
            logger.info("Программа завершена пользователем")
            
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")
        raise

if __name__ == "__main__":
    main()
