import os
from datetime import datetime

os.makedirs("logs", exist_ok=True)

LOG_FILE = "logs/app.log"


def log(msg):
    t = datetime.now().strftime("%H:%M:%S")
    line = f"[{t}] {msg}"

    with open(LOG_FILE, "a", encoding="utf8") as f:
        f.write(line + "\n")

    print(line)
