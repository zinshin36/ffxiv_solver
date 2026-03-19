import csv
import os
from engine.logger import log
from engine.runtime_paths import GAME_DATA_DIR


def normalize(s):
    return s.lower().replace("_", "").replace(" ", "")


def find_column(header, keywords):
    header_norm = [normalize(h) for h in header]

    for key in keywords:
        key = normalize(key)

        for i, col in enumerate(header_norm):
            if key in col:
                return i

    print("\n=== HEADER DEBUG DUMP ===")
    for i, col in enumerate(header):
        print(i, col)

    raise Exception(f"Column not found for {keywords}")


def load_items(min_ilvl=None):
    log("Loading Item.csv...")

    path = os.path.join(GAME_DATA_DIR, "Item.csv")

    if not os.path.exists(path):
        raise Exception("Item.csv not found")

    items = []
    max_ilvl = 0

    with open(path, encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)

        name_i = find_column(header, ["name", "singular", "itemname"])
        ilvl_i = find_column(header, ["levelitem", "ilvl"])
        slot_i = find_column(header, ["equipslotcategory"])
        materia_i = find_column(header, ["materiaslotcount"])

        log(f"[PARSER] Columns → name:{name_i} ilvl:{ilvl_i} slot:{slot_i}")

        for row_i, row in enumerate(reader):

            if row_i % 5000 == 0:
                log(f"[PARSER] Row {row_i}")

            try:
                ilvl = int(row[ilvl_i])

                if ilvl > max_ilvl:
                    max_ilvl = ilvl

                if min_ilvl and ilvl < min_ilvl:
                    continue

                item = {
                    "name": row[name_i],
                    "ilvl": ilvl,
                    "slot": row[slot_i],
                    "stats": {
                        "crit": 0,
                        "dh": 0,
                        "det": 0,
                        "sps": 0,
                        "int": 0
                    },
                    "materia_slots": int(row[materia_i])
                }

                items.append(item)

            except Exception as e:
                log(f"[PARSER ERROR] Row {row_i}: {e}")
                continue

    log(f"[PARSER] Loaded {len(items)} items (max ilvl: {max_ilvl})")

    return items, max_ilvl
