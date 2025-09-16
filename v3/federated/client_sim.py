from typing import List
import numpy as np
from v3.ai.predictive import synth_threat_features

def local_train(global_w: List[float]) -> List[float]:
	X, y = synth_threat_features(64)
	w = np.array(global_w, dtype=float)
	grad = (X.T @ (X @ w - y)) / len(X)
	return (w - 0.1 * grad).tolist()
