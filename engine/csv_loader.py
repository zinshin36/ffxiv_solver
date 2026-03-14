import csv
import os
from engine.logger import log, csv_log

DATA_DIR = "game_data"


def read_csv(name):
    path = os.path.join(DATA_DIR, name)

    if not os.path.exists(path):
        log(f"Missing CSV: {path}")
        return []

    with open(path, encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        rows = list(reader)

    if rows:
        csv_log(f"{name} columns:")
        csv_log(", ".join(rows[0]))

    return rows


def safe_int(v):
    try:
        return int(v)
    except:
        return 0
