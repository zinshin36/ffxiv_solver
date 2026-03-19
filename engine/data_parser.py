import csv
import os
from engine.logger import log
from engine.runtime_paths import GAME_DATA_DIR


def find_column(header, keywords):
    for i, col in enumerate(header):
        name = col.lower()
        for key in keywords:
            if key in name:
                return i

    log(f"[PARSER ERROR] Missing column: {keywords}")
    for i, col in enumerate(header):
        log(f"{i}: {col}")

    raise Exception(f"Column not found: {keywords}")


def load_items(min_ilvl=0):
    log("Loading Item.csv...")

    path = os.path.join(GAME_DATA_DIR, "Item.csv")

    total_rows = 0
    blm_items = 0
    final_items = []
    max_ilvl = 0

    with open(path, encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)

        name_i = find_column(header, ["name"])
        ilvl_i = find_column(header, ["levelitem"])
        job_i = find_column(header, ["classjobcategory"])

        log("[PARSER] Columns OK")

        for idx, row in enumerate(reader):
            total_rows += 1

            if idx % 5000 == 0:
                log(f"[PARSER] Row {idx}")

            try:
                ilvl = int(row[ilvl_i])
                max_ilvl = max(max_ilvl, ilvl)

                job = row[job_i]

                # COUNT BLM-LIKE ITEMS (we don’t filter hard, just count)
                if job and job != "0":
                    blm_items += 1

                if ilvl < min_ilvl:
                    continue

                final_items.append({
                    "name": row[name_i],
                    "ilvl": ilvl,
                    "slot": "unknown",
                    "job": job,
                    "stats": {},
                    "materia_slots": 0
                })

            except:
                continue

    log(f"[PARSER] TOTAL rows: {total_rows}")
    log(f"[PARSER] BLM-capable items: {blm_items}")
    log(f"[PARSER] Max iLvl: {max_ilvl}")
    log(f"[PARSER] After min iLvl filter: {len(final_items)}")

    return final_items, max_ilvl
