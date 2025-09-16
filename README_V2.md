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
