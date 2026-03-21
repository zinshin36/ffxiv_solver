import json
import os
from engine.logger import log
from engine.runtime_paths import GAME_DATA_DIR

FOOD_FILE = os.path.join(GAME_DATA_DIR, "foods.json")

def load_foods():
    foods = []

    if not os.path.exists(FOOD_FILE):
        log("[FOOD] foods.json not found")
        return foods

    try:
        with open(FOOD_FILE, encoding="utf-8") as f:
            data = json.load(f)
            for entry in data:
                stats = {}
                for key in ["crit", "dh", "det", "sps"]:
                    if key in entry:
                        stats[key] = entry[key]
                foods.append({
                    "name": entry.get("name", ""),
                    "stats": stats
                })
    except Exception as e:
        log(f"[FOOD] Failed to load foods.json: {e}")

    log(f"[FOOD] Loaded {len(foods)} foods")
    return foods

def apply_food(stats, food):
    if not food:
        return stats.copy()

    buff = food.get("stats", {})
    result = dict(stats)
    for stat, value in buff.items():
        result[stat] = result.get(stat, 0) + value
    return result
