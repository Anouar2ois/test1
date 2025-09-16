from typing import Dict, Any, List
import math


def extract_features(report: Dict[str, Any]) -> List[float]:
	"""Convert behavior report to numeric features.

	Features (example):
	- duration
	- count_stdout_chars
	- num_file_ops
	- num_net_ops
	- exit_code_nonzero
	"""
	events = report.get("events", [])
	duration = float(report.get("duration", 0.0))
	stdout_chars = sum(len(e.get("data", "")) for e in events if e.get("type") == "stdout")
	num_file = sum(1 for e in events if e.get("type") == "file_open")
	num_net = sum(1 for e in events if e.get("type") == "net_connect")
	exit_nonzero = 1.0 if any(e.get("type") == "process_exit" and e.get("code", 0) != 0 for e in events) else 0.0
	return [
		math.log1p(duration),
		math.log1p(stdout_chars),
		float(num_file),
		float(num_net),
		exit_nonzero,
	]
