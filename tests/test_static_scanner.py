from pathlib import Path
import json

from dragonshield.static_scanner import StaticScanner
from dragonshield.utils import sha256_file


def test_scanner_no_match(tmp_path: Path):
	benign = Path("samples/benign.txt")
	sigs = Path("dragonshield/signatures.json")
	scanner = StaticScanner(sigs)
	result = scanner.scan(benign)
	assert isinstance(result["sha256"], str)
	assert isinstance(result["pe_info"], dict)
	assert result["matches"] == []


def test_scanner_pattern_match(tmp_path: Path):
	sample = tmp_path / "sample.cs"
	sample.write_text("[DllImport()] void x(){}", encoding="utf-8")
	sigs = Path("dragonshield/signatures.json")
	scanner = StaticScanner(sigs)
	result = scanner.scan(sample)
	assert any(m["id"] == "SYNTH-PATTERN-1" for m in result["matches"]) 


def test_scanner_hash_match(tmp_path: Path):
	sample = tmp_path / "eicar.bin"
	sample.write_text("EICAR-SYNTHETIC-CONTENT", encoding="utf-8")
	sha = sha256_file(sample)
	# Inject a temp signature DB for this exact hash
	sigs = tmp_path / "sigs.json"
	data = {
		"version": 1,
		"signatures": [
			{"id": "TMP-HASH", "name": "Tmp.Hash", "type": "hash", "sha256": sha}
		]
	}
	sigs.write_text(json.dumps(data), encoding="utf-8")
	scanner = StaticScanner(sigs)
	result = scanner.scan(sample)
	assert any(m["id"] == "TMP-HASH" for m in result["matches"]) 
