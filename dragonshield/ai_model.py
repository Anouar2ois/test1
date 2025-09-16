from pathlib import Path
from typing import List, Dict, Any, Tuple
import json
import pickle
import random

import numpy as np
from sklearn.linear_model import LogisticRegression

from .behavior_features import extract_features


def generate_synthetic_dataset(n: int = 200) -> Tuple[np.ndarray, np.ndarray]:
	X: List[List[float]] = []
	y: List[int] = []
	for i in range(n):
		# benign-like
		dur = random.uniform(0.05, 0.5)
		stdout = random.randint(5, 150)
		files = random.randint(1, 3)
		net = random.randint(0, 1)
		exitnz = 0
		X.append([dur, stdout, files, net, exitnz])
		y.append(0)
	for i in range(n):
		# malicious-like
		dur = random.uniform(0.1, 1.0)
		stdout = random.randint(0, 30)
		files = random.randint(0, 6)
		net = random.randint(1, 4)
		exitnz = random.choice([0, 1])
		X.append([dur, stdout, files, net, exitnz])
		y.append(1)
	return np.array(X, dtype=float), np.array(y, dtype=int)


def train_model(output_path: Path) -> None:
	X, y = generate_synthetic_dataset()
	clf = LogisticRegression(max_iter=200)
	clf.fit(X, y)
	output_path.parent.mkdir(parents=True, exist_ok=True)
	with output_path.open("wb") as f:
		pickle.dump(clf, f)


def load_model(model_path: Path) -> LogisticRegression:
	with model_path.open("rb") as f:
		return pickle.load(f)


def infer_behavior(model: LogisticRegression, report: Dict[str, Any]) -> Dict[str, Any]:
	feat = np.array([extract_features(report)], dtype=float)
	proba = model.predict_proba(feat)[0][1]
	label = int(proba >= 0.5)
	return {"malicious": bool(label), "confidence": float(proba)}
