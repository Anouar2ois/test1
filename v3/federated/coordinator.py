from typing import List, Dict, Any
import numpy as np

class FedCoordinator:
	def __init__(self) -> None:
		self.global_weights = np.zeros(4)

	def assign_task(self) -> Dict[str, Any]:
		return {"model": self.global_weights.tolist(), "task": "local_train"}

	def aggregate(self, client_updates: List[List[float]]) -> List[float]:
		if not client_updates:
			return self.global_weights.tolist()
		arr = np.array(client_updates, dtype=float)
		self.global_weights = np.mean(arr, axis=0)
		return self.global_weights.tolist()
