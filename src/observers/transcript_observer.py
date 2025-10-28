from typing import Protocol


class TranscriptObserver(Protocol):
    def on_new_line(self, text: str) -> None:
        ...
