# Scalability & Roadmap

## Scale Signature Distribution
- Move from JSON to SQLite/SQLite+Delta for local, PostgreSQL for shared backend.
- Delta updates signed with publisher keys; CDN-backed distribution.

## Model Retraining
- Schedule periodic retraining on aggregated sandbox traces.
- Add drift detection and canary model deployment.

## Sandbox Hardening
- Replace simulator with isolated VM (Firecracker/QEMU) and syscall tracing (eBPF/strace) in a lab.
- Policy engine to block network and mount RO filesystems.

## Backend & UI
- Multi-tenant API with auth, rate limiting, and audit logs.
- Rich web UI and desktop agent.

## Blockchain Path
- Replace mock with local devnet; deploy Solidity contracts with Hardhat.
- Add validator staking and slashing for malicious submissions.
- Bridge to L2 for cost; IPFS/Arweave only for metadata, never raw samples.
