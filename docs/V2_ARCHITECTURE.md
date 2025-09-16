# DragonShield v2.0 Architecture

## High-level (Client-Cloud-Chain)
```mermaid
graph LR
subgraph Endpoint Clients
A1[Win/Linux/macOS Native Agent]-- upload scan -->CAPI
A2[Android Lite Scanner]-- upload scan -->CAPI
A3[Desktop UI]-- control -->CAPI
end
subgraph Cloud
CAPI[Cloud API]
CFEED[Threat Intel & Model Server]
CSBX[Sandbox Aggregator]
CK8S[(Kubernetes)]
CAPI-- updates -->A1
CAPI-- updates -->A2
CAPI-- signatures/models -->CFEED
CAPI-- traces -->CSBX
end
subgraph Blockchain
BC1[Staking & Reputation]
BC2[Rewards ERC-20]
end
CFEED-- publish metadata -->BC1
CAPI-- validator ops -->BC1
```

## Key Components
- Endpoint Agents: native Rust client + Python fallback, Android lite scanner.
- Cloud Services (FastAPI): API Gateway, Threat Intel Server, Sandbox Aggregator, Model Registry.
- Data Stores: PostgreSQL (cloud), MinIO/S3 for artifacts, Redis for queues.
- Blockchain: staking, reputation, and rewards contracts (testnet/mainnet ready).

## Flows
### Scan & Verdict (Endpoint)
1) Agent runs advanced static scan (hash, patterns, entropy, PE heuristics).
2) If unknown/risky, send sample metadata + simulated behavior report to Cloud.
3) Cloud runs AI inference (sequence model), returns verdict, pushes telemetry encrypted.

### Updates Distribution
- Cloud publishes signed signature/model delta bundles via CDN.
- Agents verify signatures, apply delta.

### Blockchain Publishing
- Validators stake, vote on signature metadata.
- Accepted entries reward submitters via ERC-20.
