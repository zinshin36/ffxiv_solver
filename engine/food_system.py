import json
import os
from engine.logger import log
from engine.runtime_paths import GAME_DATA_DIR

FOODS = {}

def load_foods():
    global FOODS
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
                    # convert flat stats to dict for consistency
                    bonus = {}
                    for stat in ["crit", "dh", "det", "sps", "int"]:
                        if stat in entry:
                            bonus[stat] = entry[stat]
                    foods.append({
                        "name": entry.get("name", ""),
                        "stats": bonus,
                        "duration": entry.get("duration", 0)
                    })
                except Exception as e:
                    log(f"[FOOD] Failed to parse entry: {e}")
    except Exception as e:
        log(f"[FOOD] Failed to load foods.json: {e}")

    FOODS = {f['name']: f for f in foods}
    log(f"[FOOD] Loaded {len(foods)} foods")
    return foods

def apply_food(stats, food_name):
    if not FOODS or food_name not in FOODS:
        return stats.copy()

    buff = FOODS[food_name]["stats"]
    result = stats.copy()
    for stat, value in buff.items():
        result[stat] = result.get(stat, 0) + value
    return result
