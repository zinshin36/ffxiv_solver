import csv
import os
from engine.logger import log
from engine.runtime_paths import GAME_DATA_DIR


def find_column(header, keywords):
    header_lower = [h.lower() for h in header]

    for i, col in enumerate(header_lower):
        for key in keywords:
            if key in col:
                return i

    log(f"[ERROR] Missing column: {keywords}")
    for i, col in enumerate(header):
        log(f"{i}: {col}")

    raise Exception(f"Column not found: {keywords}")


def load_items():
    log("Loading Item.csv...")

    path = os.path.join(GAME_DATA_DIR, "Item.csv")

    items = []
    max_ilvl = 0

    with open(path, encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)

        name_i = find_column(header, ["name"])
        ilvl_i = find_column(header, ["levelitem"])
        slot_i = find_column(header, ["equipslotcategory"])

        log(f"[PARSER] Columns OK")

        for i, row in enumerate(reader):

            if i % 5000 == 0:
                log(f"[PARSER] Row {i}")

            try:
                ilvl = int(row[ilvl_i])
                max_ilvl = max(max_ilvl, ilvl)

                items.append({
                    "name": row[name_i],
                    "ilvl": ilvl,
                    "slot": row[slot_i],
                    "stats": {},
                    "materia_slots": 2
                })

            except Exception:
                continue

    log(f"[PARSER] Loaded {len(items)} TOTAL items (max ilvl: {max_ilvl})")
    return items, max_ilvl
