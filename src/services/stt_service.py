import numpy as np
from abc import ABC, abstractmethod
from typing import Iterator
from datetime import datetime
from config.settings import settings
from src.models.transcript import TranscriptSegment, MeetingTranscript
from src.utils.logger import get_logger

logger = get_logger(__name__)

class STTService(ABC):
    @abstractmethod
    def transcribe_stream(self, audio_stream: Iterator[np.ndarray]) -> Iterator[TranscriptSegment]:
        pass

class WhisperSTTService(STTService):
    def __init__(self, model):
        self.model = model
        self.sample_rate = settings.SAMPLE_RATE
        logger.info(f"Whisper STT сервис инициализирован")
        
    def transcribe_stream(self, audio_stream: Iterator[np.ndarray]) -> Iterator[TranscriptSegment]:
        """Транскрибирует поток аудио в реальном времени"""
        buffer = np.array([], dtype=np.float32)
        buffer_duration = 0
        start_time = datetime.now()
        
        for audio_chunk in audio_stream:
            buffer = np.concatenate([buffer, audio_chunk])
            buffer_duration += len(audio_chunk) / self.sample_rate
            
            # Транскрибируем каждые 5 секунд
            if buffer_duration >= 5.0:
                try:
                    result = self.model.transcribe(
                        buffer, 
                        fp16=False,
                        task="transcribe",
                        language="ru"
                    )
                    
                    if result["text"].strip():
                        segment = TranscriptSegment(
                            start_time=0,  # Будет обновлено в контроллере
                            end_time=0,
                            text=result["text"].strip()
                        )
                        yield segment
                        
                except Exception as e:
                    logger.error(f"Ошибка транскрипции: {e}")
                
                buffer = np.array([], dtype=np.float32)
                buffer_duration = 0
