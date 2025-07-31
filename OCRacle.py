import sys
import os
from colorama import init, Fore, Style
from ocracle.core.scanner import Scanner
from ocracle.core.report import ReportWriter  # Usa il nuovo ReportWriter


def main():
    init(autoreset=True)
    print(Fore.CYAN + r"""
  ___   ____ ____            _     
 / _ \ / ___|  _ \ __ _  ___| | ___ 
| | | | |   | |_) / _` |/ __| |/ _ \
| |_| | |___|  _ < (_| | (__| |  __/
 \___/ \____|_| \_\__,_|\___|_|\___|
        
      OCRacle - Document OCR Scanner
      Author @Alessio Carletti
          
Scans a directory recursively for images/pdf documents and extracts text using OCR.
Matches extracted text against detection rules.
Outputs results in JSON and/or CSV format.
""" + Style.RESET_ALL)

    if len(sys.argv) < 2:
        print(Fore.WHITE + f"Usage: python {sys.argv[0]} <directory> [--json output.json] [--csv output.csv] [--include-text] [-v|--verbose] [--rules rules.yaml]" + Style.RESET_ALL)
        print(Fore.WHITE + "  <directory>         Directory to scan for images" + Style.RESET_ALL)
        print(Fore.WHITE + "  --json output.json  (Optional) Save results to JSON file" + Style.RESET_ALL)
        print(Fore.WHITE + "  --csv output.csv    (Optional) Save results to CSV file" + Style.RESET_ALL)
        print(Fore.WHITE + "  --include-text      (Optional) Include extracted text in the results" + Style.RESET_ALL)
        print(Fore.WHITE + "  -v / --verbose      (Optional) Show files being processed" + Style.RESET_ALL)
        print(Fore.WHITE + "  --rules file.yaml   (Optional) Custom YAML rules file" + Style.RESET_ALL)
        sys.exit(1)

    base_path = sys.argv[1]
    json_path = None
    csv_path = None
    include_text = False
    verbose = False

    # Default rules path
    default_rules_path = os.path.join(
        os.path.dirname(__file__), "ocracle", "rules", "rules.yaml"
    )
    rule_file = default_rules_path

    # Parse options
    args = sys.argv[2:]
    for i, arg in enumerate(args):
        if arg == "--json" and i + 1 < len(args):
            json_path = args[i + 1]
        if arg == "--csv" and i + 1 < len(args):
            csv_path = args[i + 1]
        if arg == "--include-text":
            include_text = True
        if arg in ("-v", "--verbose"):
            verbose = True
        if arg == "--rules" and i + 1 < len(args):
            rule_file = args[i + 1]

    # Perform the scan (pass rule_file to Scanner)
    scanner = Scanner(rule_file=rule_file)
    results = scanner.scan(base_path, include_text=include_text, verbose=verbose)

    # Use ReportWriter instead of output_writer
    report_writer = ReportWriter()
    if json_path:
        report_writer.to_json(results, json_path)
    if csv_path:
        report_writer.to_csv(results, csv_path)


if __name__ == "__main__":
    main()
