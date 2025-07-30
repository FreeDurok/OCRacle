import os
import re
from colorama import Fore, Style, init # type: ignore
from config import ESTENSIONS, RULES
from core.text_extractor import extract_text

init(autoreset=True)

def scan_directory(base_path):
    """Recursively scan a directory for matching rules."""
    matches = []
    for root, _, files in os.walk(base_path):
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext in ESTENSIONS:
                path = os.path.join(root, f)
                print(f"{Fore.CYAN}[INFO]{Style.RESET_ALL} {Fore.YELLOW}Processing file: {path}{Style.RESET_ALL}")
                text = extract_text(path)
                for rule_name, pattern in RULES.items():
                    if re.search(pattern, text, re.IGNORECASE):
                        print(f"{Fore.RED}[MATCH]{Style.RESET_ALL} {Fore.GREEN}Rule={rule_name} File={path}{Style.RESET_ALL}")
                        matches.append({"rule": rule_name, "file": path})
    return matches
