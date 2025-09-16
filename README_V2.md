# DragonShield v2.0

Production-ready plan and runnable examples with safe defaults.

## What’s New
- Advanced static scanner with entropy and heuristic scoring.
- Simulated Cuckoo/Sysmon sandbox integration points.
- Sequence AI model (heuristic or PyTorch LSTM if available).
- Cloud API v2 and Kubernetes manifests.
- Staking & reputation smart contracts (reference).
- Native Rust client prototype.
- Upgraded UI with behavior timeline.

## Run (Local Demo)
- API (endpoint): `uvicorn api.main:app --reload`
- Web v2 (mounted via API root if configured) or serve `web_v2/` statically.
- Cloud API v2 (demo): `uvicorn cloud.api_v2.main:app --port 9000`

## Security & Compliance Roadmap
- GDPR: data minimization, consent, encryption at rest/in transit (TLS + AES-GCM). Key management via KMS.
- Certifications: prepare ISMS (ISO 27001), AV-TEST/VB100 pipelines; evidence collection.
- PenTesting: quarterly external red team; sandbox escape testing with kernel hardening.

## Monetization
- Freemium tiers: Free (signatures+basic AI), Premium (real-time, fast sandbox, advanced AI).
- Partner integrations: SIEM/SOAR connectors; MSP/MSSP billing.
- Token utility: validator staking and rewards for accepted signatures.

## Upgrade Notes
- v1 components remain compatible; v2 adds new modules under `dragonshield_v2/`, `cloud/`, `deploy/`, `native/`, and enhanced `blockchain/`.

## Build & Deploy
- Docker (cloud API v2): `docker build -f docker/Dockerfile.cloud -t dragonshield/api-v2:latest .`
- Kubernetes: `kubectl apply -f deploy/k8s/api-deployment.yaml`
- Rust client: `cd native/dragonshield_rust && cargo build --release`
- Tests: `pytest -q`

## Mobile (Android)
- Prototype path: use on-device scanning via Rust core + JNI; not included here. Provide Gradle module wrapping `dragonshield_rust` in future work.

## v3.0 Update (Preview)
- Autonomous response: process isolation, rollback, network quarantine (simulated).
- Predictive security: synthetic generative/sequence model demo and federated learning coordinator/client.
- DAO governance: v3 contracts and SOC API v3 skeleton.

Quickstart (safe synthetic):
- Response engine:
```python
from v3.agent.response_engine import PolicyDecisionEngine
from pathlib import Path
e=PolicyDecisionEngine(); print(e.handle_event({"type":"net_connect","tags":["suspicious"],"pid":1234}, Path(".")))
```
- Predictive AI:
```python
from v3.ai.predictive import train_simple_predictor, infer_predictor
m=train_simple_predictor(); print(infer_predictor(m,[0.3,0.4,1,1]))
```
- Federated learning:
```python
from v3.federated.coordinator import FedCoordinator
from v3.federated.client_sim import local_train
c=FedCoordinator(); t=c.assign_task()
print(c.aggregate([local_train(t["model"]), local_train(t["model"])]))
```
- SOC API v3:
```bash
uvicorn v3.cloud.soc_api:app --reload
```

See `v3/` for sources and `deploy/v3/` for Kubernetes manifests.
