import os
import re
from datetime import datetime
from colorama import Fore, Style, init  # type: ignore
from config import ESTENSIONS, RULES
from core.text_extractor import extract_text

init(autoreset=True)

def scan_directory(base_path, include_text=False, verbose=False):
    """Sequentially scan a directory for matching rules with colored output and timing."""
    start_time = datetime.now()
    print(f"{Fore.CYAN}[*]{Style.RESET_ALL} Scan started at {Fore.YELLOW}{start_time.strftime('%Y-%m-%d %H:%M:%S')}{Style.RESET_ALL}")

    # Collect files
    files = [
        os.path.join(root, f)
        for root, _, files in os.walk(base_path)
        for f in files
        if os.path.splitext(f)[1].lower() in ESTENSIONS
    ]

    total_files = len(files)
    print(f"{Fore.CYAN}[*]{Style.RESET_ALL} Found {Fore.YELLOW}{total_files}{Style.RESET_ALL} files to process\n")

    matches = []
    match_counter = 1

    for idx, path in enumerate(files, 1):
        if verbose:
            print(f"{Fore.BLUE}--- ({idx}/{total_files}) ---{Style.RESET_ALL}")
            print(f"{Fore.CYAN}[*]{Style.RESET_ALL} {Fore.YELLOW}Processing:{Style.RESET_ALL} {path}")

        text = extract_text(path)

        for rule_name, pattern in RULES.items():
            found = [m.group(0) for m in re.finditer(pattern, text, re.IGNORECASE)]
            if found:
                count = len(found)
                print(
                    f"{Fore.CYAN}[+]{Style.RESET_ALL} {Fore.GREEN}Rule={rule_name}{Style.RESET_ALL} "
                    f"File={Fore.YELLOW}{path}{Style.RESET_ALL} "
                    f"Matches={Fore.GREEN}{count}{Style.RESET_ALL}"
                )
                entry = {
                    "index": match_counter,
                    "rule": rule_name,
                    "file": path,
                    "match_count": count,
                    "matched_text": list(set(found))
                }
                if include_text:
                    entry["text"] = text
                matches.append(entry)
                match_counter += 1

    end_time = datetime.now()
    print(f"\n{Fore.CYAN}[*]{Style.RESET_ALL} Scan finished at {Fore.YELLOW}{end_time.strftime('%Y-%m-%d %H:%M:%S')}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}[*]{Style.RESET_ALL} Duration: {Fore.YELLOW}{end_time - start_time}{Style.RESET_ALL}")

    print(f"{Fore.MAGENTA}\n[=]{Style.RESET_ALL} Total matches found: "
          f"{Fore.GREEN}{len(matches)}{Style.RESET_ALL}\n")
    return matches
