import csv
import os
import traceback
from engine.logger import log
from engine.runtime_paths import GAME_DATA_DIR

# -------------------------
# LOAD FOODS
# -------------------------
def load_foods():
    """
    Loads consumable food items from Foods.csv.
    Returns a list of dicts with name and stat bonuses.
    """
    path = os.path.join(GAME_DATA_DIR, "Foods.csv")

    if not os.path.exists(path):
        log("[FOOD] Foods.csv not found, returning empty list")
        return []

    foods = []

    try:
        with open(path, encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader)

            # find columns dynamically
            name_i = None
            stats_i = []

            header_lower = [h.lower() for h in header]

            for idx, h in enumerate(header_lower):
                if "name" in h:
                    name_i = idx
                elif any(x in h for x in ["crit", "dh", "det", "sps", "int"]):
                    stats_i.append(idx)

            if name_i is None:
                log("[FOOD] Name column not found in Foods.csv")
                return []

            for row in reader:
                try:
                    name = row[name_i].strip()
                    stats = {}
                    for i in stats_i:
                        stat_name = header[i].lower()
                        stat_value = int(float(row[i])) if row[i] else 0
                        stats[stat_name] = stat_value

                    foods.append({
                        "name": name,
                        "stats": stats
                    })
                except Exception as e:
                    log(f"[FOOD] Row parse error: {e} | row={row}")
                    continue

    except Exception as e:
        log(f"[FOOD] Failed to load Foods.csv: {e}\n{traceback.format_exc()}")
        return []

    log(f"[FOOD] Loaded {len(foods)} foods")
    return foods

# -------------------------
# SAFE TOP-LEVEL IMPORT
# -------------------------
try:
    all_foods = load_foods()
except Exception as e:
    log(f"[FOOD] Fatal error on import: {e}\n{traceback.format_exc()}")
    all_foods = []
