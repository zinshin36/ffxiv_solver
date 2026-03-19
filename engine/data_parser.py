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

    path = os.path.join(GAME_DATA_DIR, "Item.csv")

    log("Loading ALL items (no filters)...")

    with open(path, encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)

        name_i = find_column(header, ["name"])
        ilvl_i = find_column(header, ["levelitem"])
        slot_i = find_column(header, ["equipslotcategory"])
        job_i = find_column(header, ["classjobcategory"])

        total_items = 0
        usable_items = []
        max_ilvl = 0

        for i, row in enumerate(reader):

            total_items += 1

            if i % 5000 == 0:
                log(f"[PARSER] Row {i}")

            try:
                ilvl = int(row[ilvl_i])
                max_ilvl = max(max_ilvl, ilvl)

                # store RAW item
                item = {
                    "name": row[name_i],
                    "ilvl": ilvl,
                    "slot": row[slot_i],
                    "job": row[job_i],
                    "stats": {},
                    "materia_slots": 2
                }

                usable_items.append(item)

            except:
                continue

    log(f"[PARSER] TOTAL rows: {total_items}")
    log(f"[PARSER] TOTAL usable (no filter yet): {len(usable_items)}")
    log(f"[PARSER] Max iLvl: {max_ilvl}")

    return usable_items, max_ilvl
