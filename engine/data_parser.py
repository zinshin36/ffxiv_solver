import os
from engine.csv_loader import load_csv, to_int
from engine.logger import log

DATA_PATH = "game_data"


def load_all_items():
    log("Loading Item.csv...")

    rows = load_csv("Item.csv")

    header = rows[0]

    def find_col(keys):
        for i, h in enumerate(header):
            h = h.lower()
            if any(k in h for k in keys):
                return i
        return None

    name_i = find_col(["name"])
    ilvl_i = find_col(["levelitem", "itemlevel"])
    slot_i = find_col(["equipslotcategory"])
    crit_i = find_col(["criticalhit"])
    det_i = find_col(["determination"])
    dh_i = find_col(["directhit"])
    sps_i = find_col(["spellspeed"])

    items = []
    max_ilvl = 0

    for i, r in enumerate(rows[1:]):

        try:
            name = r[name_i]
            ilvl = to_int(r[ilvl_i])
            slot = r[slot_i]

            item = {
                "name": name,
                "ilvl": ilvl,
                "slot": slot,
                "crit": to_int(r[crit_i]) if crit_i else 0,
                "det": to_int(r[det_i]) if det_i else 0,
                "dh": to_int(r[dh_i]) if dh_i else 0,
                "sps": to_int(r[sps_i]) if sps_i else 0,
                "materia_slots": 2
            }

            items.append(item)

            if ilvl > max_ilvl:
                max_ilvl = ilvl

        except Exception as e:
            log(f"Row {i} skipped: {e}")

    log(f"Loaded {len(items)} items")
    log(f"Max ilvl detected: {max_ilvl}")

    return items, max_ilvl
