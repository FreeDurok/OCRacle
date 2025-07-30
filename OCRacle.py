import sys
from colorama import init, Fore, Style
from core.scanner import scan_directory
from core.output_writer import save_to_json, save_to_csv

def main():
    init(autoreset=True)
    print(Fore.RED + r"""
  ___   ____ ____            _     
 / _ \ / ___|  _ \ __ _  ___| | ___ 
| | | | |   | |_) / _` |/ __| |/ _ \
| |_| | |___|  _ < (_| | (__| |  __/
 \___/ \____|_| \_\__,_|\___|_|\___|

OCRacle - Directory OCR Scanner
Scans a directory for images/pdf documents and extracts text using OCR.
Outputs results in JSON and/or CSV format.
 
Author @Alessio Carletti Aka @Durok
""" + Style.RESET_ALL)
    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} <directory> [--json output.json] [--csv output.csv]")
        print("  <directory>         Directory to scan for images")
        print("  --json output.json  (Optional) Save results to JSON file")
        print("  --csv output.csv    (Optional) Save results to CSV file")
        sys.exit(1)

    base_path = sys.argv[1]
    json_path = None
    csv_path = None

    # Parse options
    args = sys.argv[2:]
    for i, arg in enumerate(args):
        if arg == "--json" and i + 1 < len(args):
            json_path = args[i + 1]
        if arg == "--csv" and i + 1 < len(args):
            csv_path = args[i + 1]

    # Perform the scan
    results = scan_directory(base_path)

    # Save output if requested
    if json_path:
        save_to_json(results, json_path)
    if csv_path:
        save_to_csv(results, csv_path)

if __name__ == "__main__":
    main()
