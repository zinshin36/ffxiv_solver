# engine/csv_loader.py
import os
import csv
from engine.logger import log

GAME_DATA_DIR = os.path.join(os.getcwd(), "game_data")

def load_csv(filename):
    path = os.path.join(GAME_DATA_DIR, f"{filename}.csv")
    if not os.path.exists(path):
        raise FileNotFoundError(f"{filename}.csv not found in {GAME_DATA_DIR}")
    rows = []
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    log(f"Loaded {len(rows)} rows from {filename}.csv")
    return rows

def load_items():
    return load_csv("Item")
