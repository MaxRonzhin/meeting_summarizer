"""
Модуль настроек приложения Meeting Summarizer.

Содержит конфигурационные параметры для всех компонентов системы,
включая аудио, транскрибирование и генерацию саммари.
"""

import os
from dataclasses import dataclass

@dataclass
class Settings:
    """
    Класс настроек приложения.
    
    Содержит все конфигурационные параметры, используемые
    в различных компонентах системы.
    """
    
    # Audio settings
    SAMPLE_RATE: int = 16000
    """Частота дискретизации аудио (Гц)"""
    
    CHUNK_SIZE: int = 1024
    """Размер аудио чанка для обработки"""
    
    # STT settings
    WHISPER_MODEL: str = "base"
    """Модель Whisper для транскрибирования (tiny, base, small, medium, large)"""
    
    # Summary settings
    LLM_MODEL_NAME: str = "TinyLlama-1.1B-Chat-v1.0.Q4_K_M.gguf"
    """Имя файла LLM модели"""
    
    LLM_MODEL_URL: str = "https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/TinyLlama-1.1B-Chat-v1.0.Q4_K_M.gguf"
    """URL для скачивания LLM модели"""
    
    SUMMARY_MAX_TOKENS: int = 300
    """Максимальное количество токенов в саммари"""
    
    # Logging
    LOG_LEVEL: str = "INFO"
    """Уровень логирования (DEBUG, INFO, WARNING, ERROR)"""

settings = Settings()
