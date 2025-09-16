import asyncio
from pathlib import Path
import httpx
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


def test_scan_endpoint(tmp_path: Path):
	f = tmp_path / "sample.txt"
	f.write_text("hello world", encoding="utf-8")
	with f.open("rb") as fp:
		resp = client.post("/scan", files={"file": ("sample.txt", fp, "text/plain")})
		assert resp.status_code == 200
		js = resp.json()
		assert "verdict" in js


def test_chain_publish_and_list():
	payload = {"id": "SIG-1", "name": "Test", "sha256": "abcd"}
	resp = client.post("/chain/publish", json=payload)
	assert resp.status_code == 200
	resp = client.get("/chain/signatures")
	assert resp.status_code == 200
	assert any(s.get("id") == "SIG-1" for s in resp.json()) 
