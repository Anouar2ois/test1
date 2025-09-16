from pathlib import Path
from dragonshield.sandbox import SandboxSimulator


def test_sandbox_runs(tmp_path: Path):
	sim = SandboxSimulator(tmp_path)
	report = sim.run(Path("samples/inert_program.py"))
	assert report["duration"] >= 0
	assert isinstance(report["events"], list)
	assert any(e["type"] == "process_exit" for e in report["events"])
