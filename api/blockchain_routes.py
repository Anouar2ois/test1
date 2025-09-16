from pathlib import Path
from fastapi import APIRouter
from pydantic import BaseModel
from blockchain.mock_client import MockBlockchain

router = APIRouter(prefix="/chain", tags=["blockchain"])

CHAIN_DB = Path(".chain/mock.json")
client = MockBlockchain(CHAIN_DB)


class ChainSignature(BaseModel):
	id: str
	name: str
	sha256: str | None = None
	pattern: str | None = None
	publisher: str | None = "local"


@router.get("/signatures")
def list_sigs():
	return client.list_signatures()


@router.post("/publish")
def publish(sig: ChainSignature):
	return client.publish_signature(sig.model_dump())
