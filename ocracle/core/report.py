import json
import csv
from typing import List
from ocracle.models.result import Result
from ocracle.utils import logger


class ReportWriter:
    """Handles exporting scan results to different formats."""

    def to_json(self, results: List[Result], output_path: str) -> None:
        """Public method: save results to JSON."""
        self._write_json(results, output_path)

    def to_csv(self, results: List[Result], output_path: str) -> None:
        """Public method: save results to CSV."""
        self._write_csv(results, output_path)

    def _write_json(self, results: List[Result], output_path: str) -> None:
        """Internal method: actually writes JSON file."""
        try:
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump([r.to_dict() for r in results], f, indent=4, ensure_ascii=False)
            logger.success(f"Results saved to JSON: {output_path}")
        except Exception as e:
            logger.error(f"Failed to save JSON: {e}")

    def _write_csv(self, results: List[Result], output_path: str) -> None:
        """Internal method: actually writes CSV file."""
        try:
            # Determine dynamic fieldnames
            fieldnames = ["index", "rule", "file", "match_count", "matched_text"]
            if any(r.text is not None for r in results):
                fieldnames.append("text")

            with open(output_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()

                for r in results:
                    row = r.to_dict()
                    # Convert lists and clean text
                    for k, v in row.items():
                        if isinstance(v, list):
                            row[k] = "; ".join(v)
                        elif isinstance(v, str):
                            row[k] = v.replace("\n", " ")
                    writer.writerow(row)

            logger.success(f"Results saved to CSV: {output_path}")
        except Exception as e:
            logger.error(f"Failed to save CSV: {e}")
