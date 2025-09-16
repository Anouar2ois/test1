import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, Any, List


class SandboxSimulator:
	"""Runs an inert program and simulates behavior logging.

	This does not execute untrusted code. It only runs the provided safe sample program.
	"""

	def __init__(self, work_dir: Path) -> None:
		self.work_dir = work_dir
		self.work_dir.mkdir(parents=True, exist_ok=True)

	def run(self, program: Path, timeout_seconds: int = 5) -> Dict[str, Any]:
		start = time.time()
		proc = subprocess.Popen(
			[sys.executable, str(program)],
			cwd=str(self.work_dir),
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE,
			text=True,
		)
		try:
			stdout, stderr = proc.communicate(timeout=timeout_seconds)
		except subprocess.TimeoutExpired:
			proc.kill()
			stdout, stderr = proc.communicate()

		duration = time.time() - start

		# Simulated behavior events
		events: List[Dict[str, Any]] = [
			{"type": "process_start", "cmd": [sys.executable, str(program)], "ts": start},
			{"type": "stdout", "data": stdout[:2000], "ts": start + duration / 2},
			{"type": "stderr", "data": stderr[:2000], "ts": start + duration / 2},
			{"type": "process_exit", "code": proc.returncode, "duration": duration, "ts": time.time()},
			# Synthetic file and network-like actions (simulated only)
			{"type": "file_open", "path": str(self.work_dir / "inert.log"), "result": "ok"},
			{"type": "net_connect", "dst": "203.0.113.1:80", "simulated": True, "result": "blocked"},
		]

		return {
			"program": str(program),
			"duration": duration,
			"events": events,
		}

	def write_report(self, report_path: Path, report: Dict[str, Any]) -> None:
		report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
