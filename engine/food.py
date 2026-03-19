import csv
import os
from engine.logger import log
from engine.runtime_paths import GAME_DATA_DIR

def load_foods():
    path = os.path.join(GAME_DATA_DIR, "Food.csv")
    foods = []
    if not os.path.exists(path):
        log("[FOOD] Food.csv not found")
        return foods
    with open(path, encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            try:
                foods.append({
                    "name": row[0],
                    "bonus": row[1],
                    "duration": row[2]
                })
            except:
                continue
    log(f"[FOOD] Loaded {len(foods)} foods")
    return foods
