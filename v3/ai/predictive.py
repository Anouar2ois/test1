import numpy as np
from typing import List, Dict, Any, Tuple
import random

def synth_threat_features(n: int = 256) -> Tuple[np.ndarray, np.ndarray]:
	X, y = [], []
	for _ in range(n):
		X.append([random.random()*0.2, random.random()*0.5, 0, 0]); y.append(0)
	for _ in range(n):
		X.append([random.random()*0.8+0.2, random.random()*0.8+0.2, 1, 1]); y.append(1)
	return np.array(X, dtype=float), np.array(y, dtype=int)

def train_simple_predictor() -> Dict[str, Any]:
	X, y = synth_threat_features()
	w = np.linalg.pinv(X) @ y
	return {"weights": w.tolist()}

def infer_predictor(model: Dict[str, Any], feat: List[float]) -> Dict[str, Any]:
	w = np.array(model["weights"], dtype=float)
	s = float(np.dot(np.array(feat, dtype=float), w))
	p = 1 / (1 + np.exp(-s))
	return {"prob": p, "malicious": p >= 0.5}
