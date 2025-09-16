from pathlib import Path
import sys

# Ensure repo root is on sys.path when running directly
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
	sys.path.insert(0, str(ROOT))

from dragonshield.ai_model import train_model

if __name__ == "__main__":
	train_model(Path("model_artifacts/behavior_lr.pkl"))
	print("Trained model saved to model_artifacts/behavior_lr.pkl")
