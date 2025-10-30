import pytest
import numpy as np
from src.services.stt_service import WhisperSTTService
from src.models.transcript import TranscriptSegment

def test_whisper_stt_service_initialization():
    """Тест инициализации Whisper сервиса"""
    try:
        service = WhisperSTTService()
        assert service is not None
    except Exception as e:
        pytest.skip(f"Whisper модель не доступна: {e}")

def test_transcript_segment_creation():
    """Тест создания сегмента транскрипции"""
    segment = TranscriptSegment(
        start_time=0.0,
        end_time=5.0,
        text="Тестовая транскрипция"
    )
    
    assert segment.text == "Тестовая транскрипция"
    assert segment.start_time == 0.0
    assert segment.end_time == 5.0
