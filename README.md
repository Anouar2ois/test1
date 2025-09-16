# DragonShield Antivirus (MVP)

DragonShield is an AI-powered antivirus MVP with static signature scanning, a safe dynamic sandbox simulator, behavioral AI analysis, and optional blockchain-based signature sharing (mocked locally). All examples use synthetic, harmless samples.

- Safe-by-default: no real malware execution, sandbox is simulated.
- Runnable locally: Python-based, with Docker and tests.
- Modular: static scanner, sandbox simulator, AI analyzer, optional blockchain.

## Executive Summary
DragonShield MVP demonstrates an end-to-end pipeline: static signature checks, sandbox behavior collection (simulated), AI classification, and optional signature publishing to a mock blockchain. It is designed for safe local experimentation and to provide a foundation for future hardening and productionization.

## Architecture
- Core: static scanner, sandbox simulator, behavior features, AI model.
- API: FastAPI service to scan files and manage signatures; mounts web UI.
- Blockchain (optional): mock client persisting signature metadata to a JSON file, accessible via API routes.

```
[File] -> [Static Scanner] -> [Known? Yes => Verdict]
                         -> [No] -> [Sandbox Simulator] -> [Behavior Features] -> [AI Classifier] -> Verdict
                                                          -> [Optional Publish Metadata to Mock Chain]
```

## Project Layout
```
.
├─ api/
│  ├─ main.py                # FastAPI app, mounts web UI and chain routes
│  └─ blockchain_routes.py   # Mock blockchain endpoints
├─ blockchain/
│  └─ mock_client.py         # Local JSON-backed mock chain
├─ dragonshield/
│  ├─ __init__.py
│  ├─ ai_model.py            # Synthetic training & inference
│  ├─ behavior_features.py   # Feature extraction from sandbox report
│  ├─ cli.py                 # Static scan CLI
│  ├─ orchestrator.py        # Static -> Sandbox -> AI integration
│  ├─ sandbox.py             # Safe sandbox simulator
│  ├─ sigdb_cli.py           # Signature DB CLI
│  ├─ signatures.json        # Example signatures
│  └─ static_scanner.py      # Static signature engine
├─ docker/
│  └─ Dockerfile.api
├─ scripts/
│  └─ train_ai.py            # Produces model_artifacts/behavior_lr.pkl
├─ samples/
│  ├─ benign.txt
│  ├─ inert_program.py       # Safe sample executed by sandbox
│  └─ synthetic_eicar.txt
├─ tests/
│  ├─ test_api.py
│  ├─ test_e2e.py
│  ├─ test_sandbox.py
│  └─ test_static_scanner.py
├─ web/
│  └─ index.html             # Minimal web UI
├─ .github/workflows/ci.yml  # GitHub Actions
├─ docker-compose.yml
├─ LICENSE
├─ requirements.txt
└─ README.md
```

## Run Instructions
- Install: `pip install -r requirements.txt`
- Train tiny model: `python scripts/train_ai.py`
- CLI static scan: `python -m dragonshield.cli scan samples/benign.txt`
- API: `uvicorn api.main:app --reload`
- Web UI: open `http://localhost:8000/`
- Compose: `docker-compose up --build`
- Tests: `pytest -q`

## Safety & Legal
- Do not use real malware outside an isolated lab environment you control.
- This MVP uses a sandbox simulator and synthetic data. Replacing with real analyses requires strict isolation, legal compliance, and explicit policy controls.
- Blockchain module is a mock. Do not publish sensitive data to public chains.

## Extend
- Add signatures to `dragonshield/signatures.json` or via `python -m dragonshield.sigdb_cli add --id X --name N --pattern PATTERN`.
- Replace sandbox with a real orchestrator (QEMU/Firecracker) in a lab.
- Retrain model with your traces by adapting `behavior_features.py` and `scripts/train_ai.py`.
