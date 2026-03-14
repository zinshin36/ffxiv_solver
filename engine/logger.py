import os
from datetime import datetime

os.makedirs("logs", exist_ok=True)

LOG_FILE = "logs/app.log"
CSV_LOG = "logs/csv_debug.log"


def log(msg):

    line = f"[{datetime.now().strftime('%H:%M:%S')}] {msg}"

    print(line)

    with open(LOG_FILE, "a", encoding="utf8") as f:
        f.write(line + "\n")


def csv_log(msg):

    line = f"[{datetime.now().strftime('%H:%M:%S')}] {msg}"

    with open(CSV_LOG, "a", encoding="utf8") as f:
        f.write(line + "\n")
