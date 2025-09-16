import time
from pathlib import Path

print("DragonShield inert program start")
Path("inert_output.txt").write_text("hello", encoding="utf-8")
for _ in range(3):
	print("tick")
	time.sleep(0.1)
print("DragonShield inert program end")
