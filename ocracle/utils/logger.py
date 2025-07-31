from colorama import Fore, Style, init

init(autoreset=True)

def info(message: str):
    print(f"{Fore.CYAN}[*]{Style.RESET_ALL} {message}")

def success(message: str):
    print(f"{Fore.GREEN}[+]{Style.RESET_ALL} {message}")

def warning(message: str):
    print(f"{Fore.YELLOW}[!]{Style.RESET_ALL} {message}")

def error(message: str):
    print(f"{Fore.RED}[!]{Style.RESET_ALL} {message}")

def highlight(message: str):
    """Special highlighted log (magenta)."""
    print(f"{Fore.MAGENTA}[#]{Style.RESET_ALL} {message}")

# --- Varianti block ---

def info_block(message: str):
    print(f"\n{Fore.CYAN}{Style.BRIGHT}[*] {message}{Style.RESET_ALL}")

def success_block(message: str):
    print(f"\n{Fore.GREEN}{Style.BRIGHT}[+] {message}{Style.RESET_ALL}")

def warning_block(message: str):
    print(f"\n{Fore.YELLOW}{Style.BRIGHT}[!] {message}{Style.RESET_ALL}")

def error_block(message: str):
    print(f"\n{Fore.RED}{Style.BRIGHT}[!] {message}{Style.RESET_ALL}")

def highlight_block(message: str):
    """Special highlighted log (magenta) with blank lines."""
    print(f"\n{Fore.MAGENTA}{Style.BRIGHT}[#] {message}{Style.RESET_ALL}")
