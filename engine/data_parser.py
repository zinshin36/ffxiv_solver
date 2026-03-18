import csv
import time
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


def load_all_items(path):
    log(f"STEP 1: opening file {path}")

    start_time = time.time()

    with open(path, encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        headers = next(reader)

        # Normalize headers
        norm_headers = [normalize(h) for h in headers]

        # Detect base columns
        name_col = next((i for i, h in enumerate(norm_headers) if "name" in h), 0)
        ilvl_col = next((i for i, h in enumerate(norm_headers) if "itemlevel" in h or "levelitem" in h), 0)
        slot_col = next((i for i, h in enumerate(norm_headers) if "equipslotcategory" in h or "slot" in h), 0)

        # Detect BaseParam columns (VERY IMPORTANT)
        baseparam_cols = []
        basevalue_cols = []

        for i, h in enumerate(norm_headers):
            if "baseparam" in h and "value" not in h:
                baseparam_cols.append(i)
            elif "baseparamvalue" in h:
                basevalue_cols.append(i)

        log(f"Detected {len(baseparam_cols)} BaseParam columns")

        items = []
        last_log = time.time()

        for idx, row in enumerate(reader):

            if idx % 5000 == 0:
                now = time.time()
                log(f"Loop alive at row {idx} (+{round(now-last_log,2)}s)")
                last_log = now

            try:
                stats = {"crit": 0, "dh": 0, "det": 0, "sps": 0}

                # Parse BaseParams
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
                    "slot": row[slot_col],
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
