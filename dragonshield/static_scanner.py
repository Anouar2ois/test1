from pathlib import Path
from typing import List, Dict, Any
import re

from .utils import sha256_file, read_json, pe_header_info


class StaticScanner:
	def __init__(self, signatures_path: Path) -> None:
		self.signatures = read_json(signatures_path)

	def scan(self, path: Path) -> Dict[str, Any]:
		file_hash = sha256_file(path)
		matches: List[Dict[str, Any]] = []

		for sig in self.signatures.get("signatures", []):
			if sig.get("type") == "hash" and sig.get("sha256") == file_hash:
				matches.append({"id": sig["id"], "name": sig["name"], "reason": "sha256 match"})

		# Simple pattern matching on text files only (safe; will not execute anything)
		try:
			text = path.read_text(encoding="utf-8", errors="ignore")
			for sig in self.signatures.get("signatures", []):
				if sig.get("type") == "pattern":
					pattern = sig.get("pattern", "")
					if pattern and re.search(pattern, text):
						matches.append({"id": sig["id"], "name": sig["name"], "reason": f"pattern:{pattern}"})
		except Exception:
			pass

		pe_info = pe_header_info(path)
		return {
			"sha256": file_hash,
			"pe_info": pe_info,
			"matches": matches,
		}
