from pathlib import Path
from dragonshield_v2.static_advanced import AdvancedStaticScanner
from dragonshield_v2.sandbox_orchestrator import SandboxOrchestratorV2
from dragonshield_v2.seq_model import infer_sequence


def test_advanced_static(tmp_path: Path):
	f = tmp_path / "x.bin"
	f.write_bytes(b"A" * 1000)
	scanner = AdvancedStaticScanner(Path("dragonshield/signatures.json"))
	res = scanner.scan(f)
	assert "entropy" in res and "heuristic_risk" in res


def test_seq_model_with_sandbox():
	orch = SandboxOrchestratorV2()
	report = torch.run_dynamic(Path("C:/fake.exe"))
	pred = infer_sequence(report["events"])
	assert "confidence" in pred
