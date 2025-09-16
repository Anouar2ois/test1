from pathlib import Path
from dragonshield.ai_model import train_model

if __name__ == "__main__":
	train_model(Path("model_artifacts/behavior_lr.pkl"))
	print("Trained model saved to model_artifacts/behavior_lr.pkl")
