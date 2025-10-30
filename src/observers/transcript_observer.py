"""
Наблюдатели за процессом транскрибирования.

Предоставляет интерфейсы и реализации для наблюдения
за новыми сегментами транскрипции.
"""

from abc import ABC, abstractmethod
from src.models.transcript import TranscriptSegment

class TranscriptObserver(ABC):
    """
    Абстрактный класс наблюдателя за транскрипцией.
    
    Определяет интерфейс для получения уведомлений
    о новых сегментах транскрипции.
    """
    
    @abstractmethod
    def on_new_segment(self, segment: TranscriptSegment):
        """
        Вызывается при появлении нового сегмента транскрипции.
        
        Args:
            segment: Новый сегмент транскрипции
        """
        pass

class ConsoleTranscriptObserver(TranscriptObserver):
    """
    Наблюдатель, выводящий транскрипцию в консоль.
    
    Реализует вывод новых сегментов транскрипции
    в стандартный вывод консоли.
    """
    
    def on_new_segment(self, segment: TranscriptSegment):
        """
        Выводит новый сегмент транскрипции в консоль.
        
        Args:
            segment: Новый сегмент транскрипции для вывода
        """
        print(f"[{segment.start_time:.2f}s] {segment.text}")
