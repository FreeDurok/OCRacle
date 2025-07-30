import os
import re
from colorama import Fore, Style, init  # type: ignore
from config import ESTENSIONS, RULES
from core.text_extractor import extract_text

init(autoreset=True)

def scan_directory(base_path, include_text=False):
    """Recursively scan a directory for matching rules."""
    matches = []
    match_counter = 1  # initialize counter for match IDs
    for root, _, files in os.walk(base_path):
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext in ESTENSIONS:
                path = os.path.join(root, f)
                print(f"{Fore.CYAN}[*]{Style.RESET_ALL} {Fore.YELLOW}Processing file: {path}{Style.RESET_ALL}")
                text = extract_text(path)
                for rule_name, pattern in RULES.items():
                    if re.search(pattern, text, re.IGNORECASE):
                        print(f"{Fore.CYAN}[+]{Style.RESET_ALL} {Fore.GREEN}Rule={rule_name} File={path}{Style.RESET_ALL}")
                        entry = {
                            "index": match_counter,
                            "rule": rule_name,
                            "file": path
                        }
                        if include_text:
                            entry["text"] = text
                        matches.append(entry)
                        match_counter += 1

    # Final summary
    print(f"{Fore.MAGENTA}\n[=]{Style.RESET_ALL} Total matches found: {Fore.GREEN}{len(matches)}{Style.RESET_ALL}\n")
    return matches
