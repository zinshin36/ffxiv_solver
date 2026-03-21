import csv
import os
from engine.logger import log
from engine.runtime_paths import GAME_DATA_DIR

def safe_int(v):
    try:
        return int(v)
    except:
        try:
            return int(float(v))
        except:
            return 0


def load_items(min_ilvl=0):

    path = os.path.join(GAME_DATA_DIR, "Item.csv")

    if not os.path.exists(path):
        raise Exception("Item.csv NOT FOUND")

    items = []
    max_ilvl = 0

    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            try:
                name = row.get("Name", "")
                ilvl = safe_int(row.get("LevelItem", 0))

                max_ilvl = max(max_ilvl, ilvl)

                if ilvl < min_ilvl:
                    continue

                slot = row.get("EquipSlotCategory", "")

                stats = {
                    "crit": safe_int(row.get("CriticalHit", 0)),
                    "dh": safe_int(row.get("DirectHitRate", 0)),
                    "det": safe_int(row.get("Determination", 0)),
                    "sps": safe_int(row.get("SpellSpeed", 0)),
                    "int": safe_int(row.get("Intelligence", 0)),
                }

                materia_slots = safe_int(row.get("MateriaSlotCount", 0))

                items.append({
                    "name": name,
                    "ilvl": ilvl,
                    "slot": slot,
                    "stats": stats,
                    "materia_slots": materia_slots
                })

            except:
                continue

    log(f"[PARSER] Max iLvl: {max_ilvl}")
    log(f"[PARSER] Items loaded: {len(items)}")

    return items
