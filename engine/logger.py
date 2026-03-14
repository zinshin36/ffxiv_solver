import os
from datetime import datetime

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

log_file = os.path.join(
    LOG_DIR,
    f"log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
)

def log(message):

    ts = datetime.now().strftime("%H:%M:%S")

    line = f"[{ts}] {message}"

    print(line)

    with open(log_file, "a", encoding="utf-8") as f:
        f.write(line + "\n")
