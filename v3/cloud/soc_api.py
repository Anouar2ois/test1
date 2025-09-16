from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict, Any

app = FastAPI(title="DragonShield SOC API v3")

class Incident(BaseModel):
	id: str
	severity: str
	host: str
	summary: str
	actions: List[Dict[str, Any]]

DB: Dict[str, Incident] = {}

@app.get("/incidents")
def list_incidents() -> List[Incident]:
	return list(DB.values())

@app.post("/incidents")
def create_incident(inc: Incident):
	DB[inc.id] = inc
	return {"status": "ok"}

@app.get("/rbac/roles")
def roles() -> List[str]:
	return ["viewer", "analyst", "admin"]
