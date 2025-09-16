from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict, Any

app = FastAPI(title="DragonShield SOC API v4")

class Transparency(BaseModel):
	model_version: str
	change_log: str
	authors: List[str]

TRANSPARENCY: List[Transparency] = []

@app.get("/transparency")
def list_transparency() -> List[Transparency]:
	return TRANSPARENCY

@app.post("/transparency")
def add_transparency(t: Transparency):
	TRANSPARENCY.append(t)
	return {"status": "ok"}
