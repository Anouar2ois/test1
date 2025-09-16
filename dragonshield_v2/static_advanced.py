from __future__ import annotations
from pathlib import Path
from typing import Dict, Any, List
import re
import math

from dragonshield.utils import sha256_file, read_json, pe_header_info


def shannon_entropy(data: bytes) -> float:
	if not data:
		return 0.0
	freq = {}
	for b in data:
		freq[b] = freq.get(b, 0) + 1
	n = len(data)
	return -sum((c/n) * math.log2(c/n) for c in freq.values())


SUSPICIOUS_APIS = [
	"VirtualAlloc", "WriteProcessMemory", "CreateRemoteThread",
	"RegSetValue", "InternetOpen", "URLDownloadToFile", "WinExec"
]


class AdvancedStaticScanner:
	def __init__(self, signatures_path: Path) -> None:
		self.signatures = read_json(signatures_path)

	def scan(self, path: Path) -> Dict[str, Any]:
		result: Dict[str, Any] = {}
		b = path.read_bytes()
		result["sha256"] = sha256_file(path)
		result["pe_info"] = pe_header_info(path)
		result["entropy"] = shannon_entropy(b)

		# Signature matches
		matches: List[Dict[str, Any]] = []
		for sig in self.signatures.get("signatures", []):
			if sig.get("type") == "hash" and sig.get("sha256") == result["sha256"]:
				matches.append({"id": sig["id"], "reason": "sha256"})
		if b:
			text = b.decode("utf-8", errors="ignore")
			for sig in self.signatures.get("signatures", []):
				if sig.get("type") == "pattern" and re.search(sig.get("pattern", ""), text):
					matches.append({"id": sig["id"], "reason": f"pattern:{sig['pattern']}"})
		result["matches"] = matches

		# Heuristics (simple score)
		score = 0.0
		if result["entropy"] > 7.2:  # high entropy suggests packing/obfuscation
			score += 0.5
		if result["pe_info"].get("is_pe"):
			# presence of suspicious API names in strings
			apihits = sum(1 for api in SUSPICIOUS_APIS if api in text)
			score += min(0.1 * apihits, 0.7)
		result["heuristic_score"] = round(score, 3)
		result["heuristic_risk"] = "high" if score >= 0.8 else ("medium" if score >= 0.4 else "low")
		return result
