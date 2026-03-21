import json
import os
from engine.runtime_paths import GAME_DATA_DIR

FOOD_FILE = os.path.join(GAME_DATA_DIR, "foods.json")

_foods_cache = {}

def load_foods():
    """
    Load foods from foods.json inside game_data.
    Each food entry should be like:
    {
        "name": "Popoto Potage",
        "crit": 151,
        "sps": 91
    }
    """
    global _foods_cache

    _foods_cache = {}

    if not os.path.exists(FOOD_FILE):
        print(f"[FOOD] foods.json not found at {FOOD_FILE}")
        return {}

    try:
        with open(FOOD_FILE, encoding="utf-8") as f:
            data = json.load(f)
            for entry in data:
                name = entry.get("name", "Unknown")
                stats = {}
                for stat in ["crit", "dh", "det", "sps"]:
                    if stat in entry:
                        stats[stat] = int(entry[stat])
                _foods_cache[name] = stats
        print(f"[FOOD] Loaded {_foods_cache}")
    except Exception as e:
        print(f"[FOOD] Failed to load foods.json: {e}")
        _foods_cache = {}

    return _foods_cache

def get_food_stats(name):
    """
    Return stats dict for a food name.
    Returns empty dict if not found.
    """
    return _foods_cache.get(name, {})
