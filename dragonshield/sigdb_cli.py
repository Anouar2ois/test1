import argparse
import json
from pathlib import Path


def main() -> None:
	parser = argparse.ArgumentParser(description="DragonShield Signature DB CLI")
	parser.add_argument("action", choices=["list", "add"], help="Action")
	parser.add_argument("--db", default=str(Path(__file__).parent / "signatures.json"))
	parser.add_argument("--id")
	parser.add_argument("--name")
	parser.add_argument("--sha256")
	parser.add_argument("--pattern")
	args = parser.parse_args()

	db_path = Path(args.db)
	data = json.loads(db_path.read_text(encoding="utf-8"))
	if args.action == "list":
		print(json.dumps(data, indent=2))
	elif args.action == "add":
		entry = {"id": args.id, "name": args.name}
		if args.sha256:
			entry.update({"type": "hash", "sha256": args.sha256})
		elif args.pattern:
			entry.update({"type": "pattern", "pattern": args.pattern})
		else:
			raise SystemExit("Provide --sha256 or --pattern")
		data["signatures"].append(entry)
		db_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
		print("Added")


if __name__ == "__main__":
	main()
