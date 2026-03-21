import os
import json
from engine.runtime_paths import GAME_DATA_DIR
from engine.logger import log

def load_foods():
    path = os.path.join(GAME_DATA_DIR, "foods.json")

    if not os.path.exists(path):
        log("[FOOD] foods.json NOT FOUND")
        return []

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        foods = []

        for entry in data:
            stats = {}

            for stat in ["crit", "dh", "det", "sps"]:
                if stat in entry:
                    stats[stat] = int(entry[stat])

            foods.append({
                "name": entry.get("name", "Unknown"),
                "stats": stats
            })

        log(f"[FOOD] Loaded {len(foods)} foods from foods.json")
        return foods

    except Exception as e:
        log(f"[FOOD] Failed to load foods.json: {e}")
        return []


def apply_food(stats, food_name, foods):

    if not food_name or food_name == "None":
        return stats

    for food in foods:
        if food["name"] == food_name:
            result = stats.copy()

            for stat, val in food["stats"].items():
                result[stat] = result.get(stat, 0) + val

            return result

    return stats
