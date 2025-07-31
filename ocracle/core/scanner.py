import os
from datetime import datetime
from typing import List

from ocracle.core.analyzer import FileAnalyzer
from ocracle.core.rule_engine import RuleEngine
from ocracle.core.config_manager import ConfigManager
from ocracle.utils.magic import match_magic, detect_type
from ocracle.utils import logger
from ocracle.models.result import Result


class Scanner:
    """
    Scanner for directories using magic bytes to identify files,
    extracting text and applying regex-based detection rules.
    """

    def __init__(self, rule_file: str):
        self.config = ConfigManager(rule_file=rule_file)
        self.analyzer = FileAnalyzer()
        self.rule_engine = RuleEngine(self.config.rules)
        
    def _collect_files(self, base_path: str) -> List[str]:
        """Collect files whose magic bytes match known signatures."""
        return [
            os.path.join(root, f)
            for root, _, filenames in os.walk(base_path)
            for f in filenames
            if match_magic(os.path.join(root, f))
        ]

    # def _normalize_text(self, text: str) -> str:
    #     """
    #     Normalize extracted text to improve regex matching.
    #     - Remove spaces and newlines
    #     - Convert to lowercase
    #     """
    #     return text.replace("\n", "").replace(" ", "").lower()

    def scan(self, base_path: str, include_text: bool = False, verbose: bool = False) -> List[Result]:
        """Scan a directory: detect files, extract text, apply rules."""
        start_time = datetime.now()
        logger.info_block(f"Scan started at {start_time:%Y-%m-%d %H:%M:%S}")

        files = self._collect_files(base_path)
        total = len(files)
        logger.info_block(f"Found {total} files to process")

        results: List[Result] = []
        match_counter = 1

        for idx, path in enumerate(files, 1):
            if verbose:
                logger.info(f"--- ({idx}/{total}) Processing: {path}")

            # Extract text
            file_type = detect_type(path)
            text = self.analyzer.extract_text(path, file_type)
            # normalized_text = self._normalize_text(text)

            # Apply rules through RuleEngine on normalized text
            file_results = self.rule_engine.apply_rules(
                text=text,
                file_path=path,
                start_index=match_counter,
                include_text=include_text
            )

            results.extend(file_results)
            match_counter += len(file_results)

        end_time = datetime.now()
        logger.info_block(f"Scan finished at {end_time:%Y-%m-%d %H:%M:%S}")
        logger.info_block(f"Duration: {end_time - start_time}")
        logger.success_block(f"Total matches found: {len(results)}")

        return results
