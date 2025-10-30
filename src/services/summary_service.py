"""
Сервис генерации саммари.

Предоставляет функциональность для генерации краткого содержания
встречи с использованием LLM моделей.
"""

from abc import ABC, abstractmethod
from datetime import datetime
import os
from ctransformers import AutoModelForCausalLM
from config.settings import settings
from src.utils.logger import get_logger

logger = get_logger(__name__)

class SummaryService(ABC):
    """
    Абстрактный класс сервиса генерации саммари.
    
    Определяет интерфейс для различных реализаций
    генерации саммари встреч.
    """
    
    @abstractmethod
    def summarize(self, text: str) -> str:
        """
        Генерирует саммари из текста.
        
        Args:
            text: Текст для суммаризации
            
        Returns:
            str: Сгенерированное саммари
        """
        pass

class LlamaSummaryService(SummaryService):
    """
    Сервис генерации саммари с использованием Llama модели.
    
    Использует локальную LLM для генерации краткого содержания
    транскрибированной встречи.
    """
    
    def __init__(self, model_path: str):
        """
        Инициализирует сервис с указанной моделью.
        
        Args:
            model_path: Путь к файлу модели LLM
        """
        self.model_path = model_path
        logger.info("Загрузка LLM модели...")
        try:
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_path,
                model_type="llama"
            )
            logger.info("LLM модель загружена успешно")
        except Exception as e:
            logger.error(f"Ошибка загрузки LLM: {e}")
            self.model = None
    
    def summarize(self, text: str) -> str:
        """
        Генерирует саммари из текста встречи.
        
        Args:
            text: Полный текст транскрипции встречи
            
        Returns:
            str: Сгенерированное саммари встречи
        """
        if not self.model:
            return "Ошибка: модель не загружена"
        
        prompt = f"""Создай краткое саммари встречи на основе следующего текста:

{text}

САММАРИ:"""
        
        try:
            summary = self.model(
                prompt,
                max_new_tokens=settings.SUMMARY_MAX_TOKENS,
                temperature=0.7,
                top_p=0.9,
                repetition_penalty=1.1
            )
            return summary.strip()
        except Exception as e:
            logger.error(f"Ошибка генерации саммари: {e}")
            return "Ошибка генерации саммари"
