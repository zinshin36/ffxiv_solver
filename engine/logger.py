import os
from datetime import datetime

os.makedirs("logs", exist_ok=True)

APP_LOG = "logs/app.log"
CSV_LOG = "logs/csv_debug.log"
SOLVER_LOG = "logs/solver.log"


def _write(file, msg):
    t = datetime.now().strftime("%H:%M:%S")
    line = f"[{t}] {msg}"

    with open(file, "a", encoding="utf8") as f:
        f.write(line + "\n")

    print(line)


def log(msg):
    _write(APP_LOG, msg)


def csv_log(msg):
    _write(CSV_LOG, msg)


def solver_log(msg):
    _write(SOLVER_LOG, msg)
