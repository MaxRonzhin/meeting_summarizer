"""
Модели данных для транскрипции встреч.

Содержит классы для представления сегментов транскрипции
и полной транскрипции встречи.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

@dataclass
class TranscriptSegment:
    """
    Сегмент транскрипции.
    
    Представляет одну часть транскрибированного текста
    с временной меткой и дополнительной информацией.
    
    Attributes:
        start_time: Время начала сегмента в секундах
        end_time: Время окончания сегмента в секундах
        text: Транскрибированный текст
        speaker: Идентификатор спикера (опционально)
    """
    
    start_time: float
    """Время начала сегмента в секундах от начала записи"""
    
    end_time: float
    """Время окончания сегмента в секундах от начала записи"""
    
    text: str
    """Транскрибированный текст сегмента"""
    
    speaker: Optional[str] = None
    """Идентификатор спикера (если определен)"""

@dataclass
class MeetingTranscript:
    """
    Полная транскрипция встречи.
    
    Содержит все сегменты транскрипции, метаданные встречи
    и методы для работы с полным текстом.
    
    Attributes:
        segments: Список сегментов транскрипции
        created_at: Время создания транскрипции
        duration: Длительность встречи в секундах
    """
    
    segments: List[TranscriptSegment]
    """Список всех сегментов транскрипции встречи"""
    
    created_at: datetime
    """Время создания транскрипции"""
    
    duration: float
    """Длительность встречи в секундах"""
    
    def get_full_text(self) -> str:
        """
        Возвращает полный текст транскрипции.
        
        Returns:
            str: Объединенный текст всех сегментов
        """
        return " ".join([segment.text for segment in self.segments])
    
    def get_speaker_text(self, speaker: str) -> str:
        """
        Возвращает текст всех сегментов определенного спикера.
        
        Args:
            speaker: Идентификатор спикера
            
        Returns:
            str: Текст всех сегментов указанного спикера
        """
        return " ".join([
            segment.text for segment in self.segments 
            if segment.speaker == speaker
        ])
