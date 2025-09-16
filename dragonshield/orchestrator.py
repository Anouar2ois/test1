from pathlib import Path
from typing import Dict, Any

from .static_scanner import StaticScanner
from .sandbox import SandboxSimulator
from .ai_model import load_model, infer_behavior


class Orchestrator:
	def __init__(self, signatures_path: Path, model_path: Path, work_dir: Path) -> None:
		self.scanner = StaticScanner(signatures_path)
		self.model = load_model(model_path)
		self.sandbox = SandboxSimulator(work_dir)

	def scan_file(self, file_path: Path) -> Dict[str, Any]:
		static_result = self.scanner.scan(file_path)
		if static_result["matches"]:
			return {
				"verdict": "malicious",
				"source": "static",
				"details": static_result,
				"remediation": [
					"Quarantine the file",
					"Remove startup entries",
					"Rescan after updating signatures",
				],
			}

		# Unknown by static, run sandbox simulator with inert program
		report = self.sandbox.run(Path("samples/inert_program.py"))
		ai = infer_behavior(self.model, report)
		return {
			"verdict": "malicious" if ai["malicious"] else "benign",
			"source": "ai",
			"details": {"static": static_result, "sandbox": report, "ai": ai},
			"remediation": [
				"If suspicious, isolate and rescan",
				"Update model and signatures regularly",
			],
		}
