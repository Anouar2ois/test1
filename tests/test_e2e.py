from pathlib import Path
import json
from fastapi.testclient import TestClient
from api.main import app
from dragonshield.static_scanner import StaticScanner

client = TestClient(app)


def test_e2e_static_then_api(tmp_path: Path):
	# Create a file and add its hash to signatures
	f = tmp_path / "suspicious.bin"
	f.write_text("SUSPICIOUS", encoding="utf-8")
	sigs_path = Path("dragonshield/signatures.json")
	sigs = json.loads(sigs_path.read_text(encoding="utf-8"))
	from dragonshield.utils import sha256_file
	sha = sha256_file(f)
	sigs["signatures"].append({"id": "TMP-E2E", "name": "E2E", "type": "hash", "sha256": sha})
	sigs_path.write_text(json.dumps(sigs, indent=2), encoding="utf-8")

	# Static hit via scanner directly
	scanner = StaticScanner(sigs_path)
	res = scanner.scan(f)
	assert any(m["id"] == "TMP-E2E" for m in res["matches"]) 

	# API path
	with f.open("rb") as fp:
		resp = client.post("/scan", files={"file": ("suspicious.bin", fp, "application/octet-stream")})
		assert resp.status_code == 200
		js = resp.json()
		assert js["source"] in ("static", "ai")
