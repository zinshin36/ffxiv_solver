import csv
import os
from engine.logger import log

DATA_DIR = "game_data"


def load_csv(filename):

    path = os.path.join(DATA_DIR, filename)

    if not os.path.exists(path):
        log(f"Missing CSV: {filename}")
        return []

    with open(path, encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        rows = list(reader)

    log(f"{filename} loaded ({len(rows)} rows)")

    return rows


def to_int(v):

    try:
        return int(v)
    except:
        return 0
