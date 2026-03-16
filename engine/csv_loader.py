import csv
import os
from engine.logger import log


DATA_PATH = "game_data"


def load_csv(filename):

    path = os.path.join(DATA_PATH, filename)

    if not os.path.exists(path):
        raise Exception(f"{filename} not found in game_data folder")

    rows = []

    with open(path, encoding="utf-8") as f:

        reader = csv.reader(f)

        for r in reader:
            rows.append(r)

    log(f"{filename} loaded ({len(rows)} rows)")

    return rows


def to_int(value):

    if value is None:
        return 0

    if value == "":
        return 0

    try:
        return int(value)

    except:
        try:
            return int(float(value))
        except:
            return 0
