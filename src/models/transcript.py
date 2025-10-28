from dataclasses import dataclass, field
from typing import List


@dataclass
class Transcript:
    lines: List[str] = field(default_factory=list)

    def add_line(self, text: str) -> None:
        self.lines.append(text)
