import csv
import os

DATA_DIR = "game_data"


def csv_path(name):
    return os.path.join(DATA_DIR, name)


def load_csv(name):

    path = csv_path(name)

    if not os.path.exists(path):
        raise Exception(f"{name} not found in game_data")

    with open(path, encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        rows = list(reader)

    print(f"{name} loaded ({len(rows)} rows)")

    return rows


def find_col(header, text):

    text = text.lower()

    for i, col in enumerate(header):
        if text in col.lower():
            return i

    raise Exception(f"Column containing '{text}' not found")


def to_int(v):

    if v is None:
        return 0

    v = str(v).strip()

    if v == "":
        return 0

    try:
        return int(float(v))
    except:
        return 0
