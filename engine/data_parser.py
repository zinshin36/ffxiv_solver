import csv
import time
import os
from engine.logger import log


def safe_int(val):
    try:
        if val is None or val == "":
            return 0
        return int(float(val))
    except:
        return 0


def normalize(h):
    return h.lower().replace("_", "").replace(" ", "")


def load_slot_map(path):
    log("Loading EquipSlotCategory...")

    slot_map = {}

    with open(path, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)

        for row in reader:
            slot_id = row.get("Key")

            # These flags exist in SaintCoinach export
            if row.get("MainHand") == "True":
                slot_map[slot_id] = "weapon"
            elif row.get("Head") == "True":
                slot_map[slot_id] = "head"
            elif row.get("Body") == "True":
                slot_map[slot_id] = "body"
            elif row.get("Hands") == "True":
                slot_map[slot_id] = "hands"
            elif row.get("Legs") == "True":
                slot_map[slot_id] = "legs"
            elif row.get("Feet") == "True":
                slot_map[slot_id] = "feet"
            elif row.get("Ears") == "True":
                slot_map[slot_id] = "earrings"
            elif row.get("Neck") == "True":
                slot_map[slot_id] = "necklace"
            elif row.get("Wrists") == "True":
                slot_map[slot_id] = "bracelet"
            elif row.get("FingerL") == "True" or row.get("FingerR") == "True":
                slot_map[slot_id] = "ring"

    log(f"Loaded {len(slot_map)} slot mappings")
    return slot_map


def load_all_items(item_path):
    log(f"STEP 1: opening file {item_path}")

    slot_map = load_slot_map(os.path.join("game_data", "EquipSlotCategory.csv"))

    start_time = time.time()

    with open(item_path, encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        headers = next(reader)

        norm_headers = [normalize(h) for h in headers]

        name_col = next(i for i, h in enumerate(norm_headers) if "name" in h)
        ilvl_col = next(i for i, h in enumerate(norm_headers) if "itemlevel" in h)
        slot_col = next(i for i, h in enumerate(norm_headers) if "equipslotcategory" in h)

        baseparam_cols = []
        basevalue_cols = []

        for i, h in enumerate(norm_headers):
            if "baseparam" in h and "value" not in h:
                baseparam_cols.append(i)
            elif "baseparamvalue" in h:
                basevalue_cols.append(i)

        items = []
        last_log = time.time()

        for idx, row in enumerate(reader):

            if idx % 5000 == 0:
                now = time.time()
                log(f"Loop alive at row {idx} (+{round(now-last_log,2)}s)")
                last_log = now

            try:
                slot_id = row[slot_col]
                real_slot = slot_map.get(slot_id)

                if not real_slot:
                    continue

                stats = {"crit": 0, "dh": 0, "det": 0, "sps": 0}

                for p_col, v_col in zip(baseparam_cols, basevalue_cols):
                    param = normalize(row[p_col]) if p_col < len(row) else ""
                    val = safe_int(row[v_col]) if v_col < len(row) else 0

                    if "criticalhit" in param:
                        stats["crit"] += val
                    elif "directhit" in param:
                        stats["dh"] += val
                    elif "determination" in param:
                        stats["det"] += val
                    elif "spellspeed" in param:
                        stats["sps"] += val

                item = {
                    "name": row[name_col],
                    "ilvl": safe_int(row[ilvl_col]),
                    "slot": real_slot,
                    "crit": stats["crit"],
                    "dh": stats["dh"],
                    "det": stats["det"],
                    "sps": stats["sps"],
                    "materia_slots": 2
                }

                items.append(item)

            except Exception as e:
                log(f"Row {idx} ERROR: {e}")
                continue

    log(f"Total items parsed: {len(items)}")
    log(f"TOTAL TIME: {round(time.time() - start_time,2)}s")

    return items
