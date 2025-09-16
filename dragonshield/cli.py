import argparse
from pathlib import Path
import json

from .static_scanner import StaticScanner


def main() -> None:
	parser = argparse.ArgumentParser(description="DragonShield CLI")
	parser.add_argument("scan", nargs="?", help="Scan a file path")
	parser.add_argument("path", nargs="?", help="Path to file to scan")
	parser.add_argument("--sigs", default=str(Path(__file__).parent / "signatures.json"), help="Path to signatures JSON")
	args = parser.parse_args()

	if args.scan == "scan" and args.path:
		scanner = StaticScanner(Path(args.sigs))
		result = scanner.scan(Path(args.path))
		print(json.dumps(result, indent=2))
	else:
		parser.print_help()


if __name__ == "__main__":
	main()
