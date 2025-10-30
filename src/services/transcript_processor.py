import re
from typing import List
from src.models.transcript import TranscriptSegment
from src.utils.logger import get_logger

logger = get_logger(__name__)

class TranscriptProcessor:
    def clean_text(self, text: str) -> str:
        """Очищает текст от лишних символов"""
        # Удаляем лишние пробелы
        text = re.sub(r'\s+', ' ', text)
        # Удаляем повторяющиеся знаки препинания
        text = re.sub(r'[.!?]{2,}', '.', text)
        return text.strip()
    
    def detect_speakers(self, segments: List[TranscriptSegment]) -> List[TranscriptSegment]:
        """Пытается определить спикеров (упрощенная реализация)"""
        # В реальной реализации можно использовать диаризацию
        for i, segment in enumerate(segments):
            segment.speaker = f"Спикер {i % 2 + 1}"
        return segments
    
    def process_segments(self, segments: List[TranscriptSegment]) -> List[TranscriptSegment]:
        """Обрабатывает сегменты транскрипции"""
        processed_segments = []
        
        for segment in segments:
            cleaned_text = self.clean_text(segment.text)
            if cleaned_text:
                segment.text = cleaned_text
                processed_segments.append(segment)
        
        return self.detect_speakers(processed_segments)
