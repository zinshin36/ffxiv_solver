import os
from datetime import datetime

os.makedirs("logs", exist_ok=True)

LOG_FILE = "logs/app.log"
CSV_LOG = "logs/csv_debug.log"
SOLVER_LOG = "logs/solver.log"


def _write(file, msg):
    line = f"[{datetime.now().strftime('%H:%M:%S')}] {msg}"
    with open(file, "a", encoding="utf8") as f:
        f.write(line + "\n")
    return line


def log(msg):
    line = _write(LOG_FILE, msg)
    print(line)


def csv_log(msg):
    _write(CSV_LOG, msg)


def solver_log(msg):
    _write(SOLVER_LOG, msg)
