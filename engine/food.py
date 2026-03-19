import json
import os
from engine.logger import log
from engine.runtime_paths import GAME_DATA_DIR

def load_foods():
    path = os.path.join(GAME_DATA_DIR, "foods.json")
    foods = []

    if not os.path.exists(path):
        log("[FOOD] foods.json not found")
        return foods

    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
            for entry in data:
                try:
                    foods.append({
                        "name": entry.get("name", ""),
                        "bonus": entry.get("bonus", {}),
                        "duration": entry.get("duration", 0)
                    })
                except Exception as e:
                    log(f"[FOOD] Failed to parse entry: {e}")
    except Exception as e:
        log(f"[FOOD] Failed to load foods.json: {e}")

    log(f"[FOOD] Loaded {len(foods)} foods")
    return foods
