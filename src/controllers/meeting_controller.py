from src.services import AudioCapture, STTService, TranscriptProcessor, SummaryService
from src.utils.logger import get_logger


class MeetingController:
    def __init__(self) -> None:
        self.logger = get_logger(__name__)
        self.audio_capture = AudioCapture()
        self.stt_service = STTService()
        self.transcript_processor = TranscriptProcessor()
        self.summary_service = SummaryService()

    def run(self) -> None:
        self.logger.info("Meeting summarizer started")
        audio_stream = self.audio_capture.stream()
        transcript_lines = self.stt_service.transcribe_stream(audio_stream)
        processed = self.transcript_processor.process(transcript_lines)
        summary = self.summary_service.summarize(processed)
        self.logger.info("Summary generated: %s", summary)
