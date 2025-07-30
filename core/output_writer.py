import json
import csv
from pathlib import Path
from colorama import Fore, Style, init

init(autoreset=True)

def save_to_json(results, output_path):
    """Save matches to a JSON file."""
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=4, ensure_ascii=False)
        print(f"{Fore.CYAN}[+]{Style.RESET_ALL} {Fore.GREEN}Results saved to JSON:{Style.RESET_ALL} {output_path}")
    except Exception as e:
        print(f"{Fore.RED}[!] Failed to save JSON:{Style.RESET_ALL} {e}")

def save_to_csv(results, output_path):
    """Save matches to a CSV file."""
    try:
        # Base fieldnames (ordered)
        fieldnames = ["index", "rule", "file", "match_count", "matched_text"]

        # Add 'text' column if at least one record contains it
        if any("text" in r for r in results):
            fieldnames.append("text")

        with open(output_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for r in results:
                row = {}
                for k in fieldnames:
                    if k in r:
                        val = r[k]
                        # Convert lists (like matched_text) to semicolon-separated strings
                        if isinstance(val, list):
                            val = "; ".join(val)
                        elif isinstance(val, str):
                            val = val.replace("\n", " ")
                        row[k] = val
                writer.writerow(row)

        print(f"{Fore.CYAN}[+]{Style.RESET_ALL} {Fore.GREEN}Results saved to CSV:{Style.RESET_ALL} {output_path}")
    except Exception as e:
        print(f"{Fore.RED}[!] Failed to save CSV:{Style.RESET_ALL} {e}")
