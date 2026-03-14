import csv
import os
from engine.logger import csv_log

DATA_DIR = "game_data"


def load_csv(name):

    path = os.path.join(DATA_DIR, name)

    with open(path, encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        rows = list(reader)

    if rows:
        csv_log(f"{name} columns:")
        csv_log(",".join(rows[0]))

    return rows


def i(x):
    try:
        return int(x)
    except:
        return 0
