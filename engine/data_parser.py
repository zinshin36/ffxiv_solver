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

    log(f"[PARSER ERROR] Missing column for {keywords}")
    for i, col in enumerate(header):
        log(f"{i}: {col}")

    raise Exception(f"Column not found: {keywords}")


def load_items(min_ilvl=0):
    log("Loading Item.csv...")

    path = os.path.join(GAME_DATA_DIR, "Item.csv")

    items = []
    total_rows = 0
    max_ilvl = 0

    with open(path, encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)

        name_i = find_column(header, ["name"])
        ilvl_i = find_column(header, ["levelitem"])
        slot_i = find_column(header, ["equipslotcategory"])
        job_i = find_column(header, ["classjobcategory"])
        materia_i = find_column(header, ["materiaslotcount"])

        param_indices = [i for i, c in enumerate(header) if "baseparam[" in c.lower()]
        value_indices = [i for i, c in enumerate(header) if "baseparamvalue[" in c.lower()]

        log("[PARSER] Columns OK")

        for idx, row in enumerate(reader):
            total_rows += 1

            if idx % 5000 == 0:
                log(f"[PARSER] Row {idx}")

            try:
                ilvl = int(row[ilvl_i])
                max_ilvl = max(max_ilvl, ilvl)

                if ilvl < min_ilvl:
                    continue

                stats = {"crit": 0, "dh": 0, "det": 0, "sps": 0, "int": 0}

                for p_i, v_i in zip(param_indices, value_indices):
                    try:
                        val = int(row[v_i])
                        stats["int"] += val  # fallback (no param mapping)
                    except:
                        continue

                items.append({
                    "name": row[name_i],
                    "ilvl": ilvl,
                    "slot": row[slot_i],
                    "job": row[job_i],
                    "stats": stats,
                    "materia_slots": int(row[materia_i] or 0)
                })

            except:
                continue

    log(f"[PARSER] TOTAL items: {total_rows}")
    log(f"[PARSER] Max iLvl: {max_ilvl}")
    log(f"[PARSER] After min iLvl filter: {len(items)}")

    return items, max_ilvl
