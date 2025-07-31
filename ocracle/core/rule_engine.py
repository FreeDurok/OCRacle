import re
from typing import List
from ocracle.models.result import Result
from ocracle.utils import logger


class RuleEngine:
    """Applies regex-based rules to extracted text."""

    def __init__(self, rules: dict[str, str]):
        # salva le regole (dict nome -> regex)
        self.rules = rules

    def apply_rules(
        self,
        text: str,
        file_path: str,
        start_index: int = 1,
        include_text: bool = False
    ) -> List[Result]:
        """Apply all rules to a text and return a list of Result."""
        results: List[Result] = []
        index = start_index

        for rule_name, pattern in self.rules.items():
            matches = [m.group(0) for m in re.finditer(pattern, text, re.IGNORECASE)]
            if matches:
                match_count = len(matches)
                logger.success(
                    f"Rule={rule_name} File={file_path} Matches={match_count}"
                )
                result = Result(
                    index=index,
                    rule=rule_name,
                    file=file_path,
                    match_count=match_count,
                    matched_text=list(set(matches)),
                    text=text if include_text else None,
                )
                results.append(result)
                index += 1

        return results
