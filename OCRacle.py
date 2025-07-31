import argparse
from colorama import init, Fore, Style
from ocracle.core.scanner import Scanner
from ocracle.core.report import ReportWriter
from ocracle.utils.formatter import ColorHelpFormatter
from ocracle.config.config import default_rules_path



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
""" + Style.RESET_ALL)

    parser = argparse.ArgumentParser(
        description=f"{Fore.CYAN}Recursively scan a directory for documents (PDF/images) and detect sensitive data.{Style.RESET_ALL}",
        formatter_class=ColorHelpFormatter
    )
    parser.add_argument("directory", help="Directory to scan for images and PDFs")
    parser.add_argument("--json", dest="json_path", help="Save results to JSON file")
    parser.add_argument("--csv", dest="csv_path", help="Save results to CSV file")
    parser.add_argument("--include-text", action="store_true", help="Include full extracted text in results")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show files being processed")
    parser.add_argument("--rules", dest="rule_file", default=default_rules_path,
                        help=f"Custom YAML rules file (default: {default_rules_path})")

    args = parser.parse_args()

    # Perform the scan
    scanner = Scanner(rule_file=args.rule_file)
    results = scanner.scan(args.directory, include_text=args.include_text, verbose=args.verbose)

    # Export
    report_writer = ReportWriter()
    if args.json_path:
        report_writer.to_json(results, args.json_path)
    if args.csv_path:
        report_writer.to_csv(results, args.csv_path)


if __name__ == "__main__":
    main()
