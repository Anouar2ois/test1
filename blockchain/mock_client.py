from pathlib import Path
from typing import Dict, Any, List
import json
import time


class MockBlockchain:
	def __init__(self, db_path: Path) -> None:
		self.db_path = db_path
		self.db_path.parent.mkdir(parents=True, exist_ok=True)
		if not self.db_path.exists():
			self._write({"signatures": [], "validators": {}})

	def _read(self) -> Dict[str, Any]:
		return json.loads(self.db_path.read_text(encoding="utf-8"))

	def _write(self, data: Dict[str, Any]) -> None:
		self.db_path.write_text(json.dumps(data, indent=2), encoding="utf-8")

	def publish_signature(self, meta: Dict[str, Any]) -> Dict[str, Any]:
		data = self._read()
		entry = {
			"id": meta.get("id"),
			"name": meta.get("name"),
			"sha256": meta.get("sha256"),
			"pattern": meta.get("pattern"),
			"publisher": meta.get("publisher", "local"),
			"ts": time.time(),
			"votes": 0,
		}
		data["signatures"].append(entry)
		self._write(data)
		return entry

	def list_signatures(self) -> List[Dict[str, Any]]:
		return self._read().get("signatures", [])
