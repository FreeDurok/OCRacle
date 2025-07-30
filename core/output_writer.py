import json
import csv
from pathlib import Path

def save_to_json(results, output_path):
    """Save matches to a JSON file."""
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=4, ensure_ascii=False)
        print(f"[+] Results saved to JSON: {output_path}")
    except Exception as e:
        print(f"[!] Failed to save JSON: {e}")

def save_to_csv(results, output_path):
    """Save matches to a CSV file."""
    try:
        with open(output_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["rule", "file"])
            writer.writeheader()
            for r in results:
                writer.writerow(r)
        print(f"[+] Results saved to CSV: {output_path}")
    except Exception as e:
        print(f"[!] Failed to save CSV: {e}")
