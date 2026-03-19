import csv
import os
from engine.logger import log
from engine.runtime_paths import GAME_DATA_DIR

# -------------------------
# FOOD LOADER
# -------------------------
def load_foods():
    path = os.path.join(GAME_DATA_DIR, "Foods.csv")
    foods = []

    if not os.path.exists(path):
        log(f"[FOOD] File not found: {path}")
        return foods

    try:
        with open(path, encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader)

            # Flexible column detection
            name_i = None
            stats_start = None

            for i, col in enumerate(header):
                col_l = col.lower()
                if "name" in col_l:
                    name_i = i
                if "baseparamvalue" in col_l or "value" in col_l:
                    stats_start = i
                    break

            if name_i is None:
                log("[FOOD] No 'name' column found in Foods.csv")
                return foods

            for row in reader:
                try:
                    name = row[name_i]
                    stats = {}

                    if stats_start is not None:
                        for i in range(stats_start, len(row)):
                            if row[i].strip() != "":
                                stats[f"value{i-stats_start}"] = int(float(row[i]))

                    foods.append({
                        "name": name,
                        "stats": stats
                    })
                except:
                    continue

    except Exception as e:
        log(f"[FOOD] Error reading Foods.csv: {e}")

    log(f"[FOOD] Foods loaded: {len(foods)}")
    return foods
