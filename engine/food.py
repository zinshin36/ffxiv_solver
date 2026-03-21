import json
import os
from engine.runtime_paths import GAME_DATA_DIR
from engine.logger import log

FOOD_FILE = os.path.join(GAME_DATA_DIR, "foods.json")

def load_foods():
    """
    Load foods from foods.json. Each food must have a "name" and stat keys like "crit", "dh", "det", "sps".
    Returns a list of food dictionaries.
    """
    foods = []
    if not os.path.exists(FOOD_FILE):
        log("[FOOD] foods.json not found")
        return foods

    try:
        with open(FOOD_FILE, encoding="utf-8") as f:
            data = json.load(f)
            for entry in data:
                # Ensure there's a name
                name = entry.get("name")
                if not name:
                    continue
                # Only keep valid stat keys
                stats = {k: v for k, v in entry.items() if k.lower() in ["crit", "dh", "det", "sps"]}
                foods.append({"name": name, "stats": stats})
    except Exception as e:
        log(f"[FOOD] Failed to load foods.json: {e}")

    log(f"[FOOD] Loaded {len(foods)} foods")
    return foods
