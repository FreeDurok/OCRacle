from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Result:
    """
    Represents a single result (rule matched in a file) produced by the scanner.
    """
    index: int
    rule: str
    file: str
    match_count: int
    matched_text: List[str] = field(default_factory=list)
    text: Optional[str] = None  # full extracted text (optional)

    def to_dict(self) -> dict:
        """Convert the result to a dictionary for serialization."""
        data = {
            "index": self.index,
            "rule": self.rule,
            "file": self.file,
            "match_count": self.match_count,
            "matched_text": self.matched_text,
        }
        if self.text is not None:
            data["text"] = self.text
        return data
