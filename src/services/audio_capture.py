"""
Сервис захвата аудио.

Предоставляет функциональность для захвата аудио
с локального устройства в реальном времени.
"""

import sounddevice as sd
import numpy as np
from typing import Iterator
from config.settings import settings
from src.utils.logger import get_logger

logger = get_logger(__name__)

class AudioCaptureService:
    """
    Сервис захвата аудио с локального устройства.
    
    Использует sounddevice для захвата аудио потока
    с микрофона или других аудиоустройств.
    """
    
    def __init__(self):
        """
        Инициализирует сервис захвата аудио.
        
        Устанавливает параметры захвата из настроек.
        """
        self.sample_rate = settings.SAMPLE_RATE
        self.chunk_size = settings.CHUNK_SIZE
        self.is_recording = False
        logger.info("AudioCaptureService инициализирован")
        
    def start_capture(self) -> Iterator[np.ndarray]:
        """
        Начинает захват аудио и возвращает поток данных.
        
        Returns:
            Iterator[np.ndarray]: Итератор аудио данных
            
        Yields:
            np.ndarray: Чанк аудио данных в формате numpy массива
        """
        logger.info("Начало захвата аудио")
        self.is_recording = True
        
        with sd.InputStream(
            samplerate=self.sample_rate,
            channels=1,
            dtype=np.float32,
            blocksize=self.chunk_size
        ) as stream:
            while self.is_recording:
                data, overflowed = stream.read(self.chunk_size)
                if overflowed:
                    logger.warning("Аудио буфер переполнен")
                yield data.flatten()
    
    def stop_capture(self):
        """
        Останавливает захват аудио.
        
        Завершает процесс захвата и освобождает ресурсы.
        """
        logger.info("Остановка захвата аудио")
        self.is_recording = False
