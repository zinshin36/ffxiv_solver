import csv
import os
from engine.logger import log

DATA_PATH = "game_data"


def load_csv(filename):

    path = os.path.join(DATA_PATH, filename)

    if not os.path.exists(path):
        raise Exception(f"{filename} not found in game_data folder")

    rows = []

    with open(path, encoding="utf-8-sig") as f:
        reader = csv.reader(f)

        for r in reader:
            rows.append([c.strip() if c else "" for c in r])

    log(f"{filename} loaded ({len(rows)} rows)")

    return rows


def to_int(v):

    if v is None:
        return 0

    if isinstance(v, int):
        return v

    if isinstance(v, float):
        return int(v)

    if isinstance(v, str):

        v = v.strip()

        if v == "":
            return 0

        try:
            return int(v)
        except:
            try:
                return int(float(v))
            except:
                return 0

    return 0
