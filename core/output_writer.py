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
        # Determine fieldnames dynamically: always index, rule and file; add text if present
        fieldnames = ["index", "rule", "file"]
        if any("text" in r for r in results):
            fieldnames.append("text")

        with open(output_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for r in results:
                r_clean = {k: (v.replace('\n', ' ') if isinstance(v, str) else v)
                           for k, v in r.items() if k in fieldnames}
                writer.writerow(r_clean)

        print(f"{Fore.CYAN}[+]{Style.RESET_ALL} {Fore.GREEN}Results saved to CSV:{Style.RESET_ALL} {output_path}")
    except Exception as e:
        print(f"{Fore.RED}[!] Failed to save CSV:{Style.RESET_ALL} {e}")
