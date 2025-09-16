from pathlib import Path
from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import tempfile
import json

from dragonshield.orchestrator import Orchestrator
from .blockchain_routes import router as chain_router

app = FastAPI(title="DragonShield API")

SIGS = Path("dragonshield/signatures.json")
MODEL = Path("model_artifacts/behavior_lr.pkl")
WORK = Path(".sandbox")

orch = Orchestrator(SIGS, MODEL, WORK)


class Signature(BaseModel):
	id: str
	name: str
	type: str
	sha256: str | None = None
	pattern: str | None = None


@app.post("/scan")
async def scan(file: UploadFile = File(...)):
	tmp_path: Path | None = None
	try:
		content = await file.read()
		with tempfile.NamedTemporaryFile(delete=False) as tmp:
			tmp.write(content)
			tmp.flush()
			tmp_path = Path(tmp.name)
		result = orch.scan_file(tmp_path)
		return result
	finally:
		if tmp_path is not None and tmp_path.exists():
			try:
				tmp_path.unlink()
			except Exception:
				pass


app.include_router(chain_router)

# Serve static web UI from / if available
WEB_DIR = Path("web")
if WEB_DIR.exists():
	app.mount("/", StaticFiles(directory=str(WEB_DIR), html=True), name="web")


@app.post("/signatures")
async def push_signature(sig: Signature):
	data = json.loads(Path(SIGS).read_text(encoding="utf-8"))
	data["signatures"].append(sig.model_dump())
	Path(SIGS).write_text(json.dumps(data, indent=2), encoding="utf-8")
	return {"status": "ok"}
