from __future__ import annotations
from typing import List, Dict, Any
import math
import random

try:
	import torch
	import torch.nn as nn
	TORCH_AVAILABLE = True
except Exception:
	TORCH_AVAILABLE = False


EVENT_EMBED = {
	1: 0.2,  # process create
	3: 0.7,  # network connect
	11: 0.5, # file write
}


def simple_seq_score(events: List[Dict[str, Any]]) -> float:
	# Heuristic: more net connects + file writes => higher risk
	score = 0.0
	for e in events:
		w = EVENT_EMBED.get(int(e.get("EventID", 0)), 0.1)
		score += w
	return 1 - math.exp(-score)


class TorchRNN(nn.Module):
	def __init__(self):
		super().__init__()
		self.rnn = nn.LSTM(input_size=1, hidden_size=8, num_layers=1, batch_first=True)
		self.fc = nn.Linear(8, 1)
		self.sig = nn.Sigmoid()
	def forward(self, x):
		out, _ = self.rnn(x)
		out = out[:, -1, :]
		return self.sig(self.fc(out))


def infer_sequence(events: List[Dict[str, Any]]) -> Dict[str, Any]:
	if TORCH_AVAILABLE:
		model = TorchRNN()
		with torch.no_grad():
			seq = [EVENT_EMBED.get(int(e.get("EventID", 0)), 0.1) for e in events]
			t = torch.tensor(seq, dtype=torch.float32).view(1, -1, 1)
			p = float(model(t).item())
			return {"malicious": p >= 0.5, "confidence": p, "engine": "torch-lstm"}
	else:
		p = simple_seq_score(events)
		return {"malicious": p >= 0.5, "confidence": p, "engine": "heuristic-seq"}
