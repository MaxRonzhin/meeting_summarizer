import pytest

from src.services.stt_service import STTService


def test_stt_service_transcribe_stream_empty_iterable():
    service = STTService()
    result = service.transcribe_stream([])
    assert isinstance(result, list)
    assert result == []
