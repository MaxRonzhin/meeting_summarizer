from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

APP_NAME = "meeting_summarizer"
DEBUG = True

LOG_LEVEL = "INFO"
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

# STT/LLM providers placeholders
STT_PROVIDER = "stub"
SUMMARY_PROVIDER = "stub"
