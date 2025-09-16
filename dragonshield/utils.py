import hashlib
import json
from pathlib import Path
from typing import Dict, Any

import pefile


def sha256_file(path: Path) -> str:
	sha256 = hashlib.sha256()
	with path.open("rb") as f:
		for chunk in iter(lambda: f.read(8192), b""):
			sha256.update(chunk)
	return sha256.hexdigest()


def read_json(path: Path) -> Any:
	with path.open("r", encoding="utf-8") as f:
		return json.load(f)


def write_json(path: Path, data: Any) -> None:
	with path.open("w", encoding="utf-8") as f:
		json.dump(data, f, indent=2, ensure_ascii=False)


def pe_header_info(path: Path) -> Dict[str, Any]:
	info: Dict[str, Any] = {}
	try:
		pe = pefile.PE(str(path))
		info["is_pe"] = True
		info["machine"] = hex(pe.FILE_HEADER.Machine)
		info["num_sections"] = len(pe.sections)
		info["entry_point"] = hex(pe.OPTIONAL_HEADER.AddressOfEntryPoint)
		info["dll"] = bool(pe.FILE_HEADER.Characteristics & 0x2000)
	except Exception:
		info["is_pe"] = False
	return info
