import csv
import time
from engine.logger import log

def safe_int(val):
    try:
        return int(val)
    except:
        return 0


def parse_items(path="game_data/Item.csv"):
    """
    Parses Item.csv from SaintCoinach/Godbert
    Only minimal work here; returns all items as dicts
    """
    log("DATA_PARSER IMPORTED")
    start_time = time.time()
    items = []

    if not path or not path.endswith(".csv"):
        log("Invalid path for items")
        return []

    log(f"STEP 1: opening file {path}")
    try:
        f = open(path, encoding="utf-8-sig", newline="")
    except Exception as e:
        log(f"ERROR opening file: {e}")
        return []

    reader = csv.reader(f)
    try:
        headers = next(reader)
    except Exception as e:
        log(f"ERROR reading headers: {e}")
        return []

    # Detect columns
    header_norm = [h.lower() for h in headers]
    def find_idx(keys):
        for i, h in enumerate(header_norm):
            if any(k in h for k in keys):
                return i
        return None

    name_i = find_idx(["name"])
    ilvl_i = find_idx(["levelitem", "itemlevel"])
    slot_i = find_idx(["equipslotcategory"])
    stats_i = {
        "crit": find_idx(["criticalhit"]),
        "dh": find_idx(["directhit"]),
        "det": find_idx(["determination"]),
        "sps": find_idx(["spellspeed"])
    }

    log(f"Columns detected: name={name_i}, ilvl={ilvl_i}, slot={slot_i}, stats={stats_i}")

    last_log = time.time()
    for i, row in enumerate(reader):
        if i % 5000 == 0:
            log(f"Loop alive at row {i} (+{round(time.time() - last_log, 2)}s)")
            last_log = time.time()
        try:
            name = row[name_i] if name_i is not None else "Unknown"
            ilvl = safe_int(row[ilvl_i]) if ilvl_i is not None else 0
            slot = row[slot_i] if slot_i is not None else None
            stats = {}
            for k, idx in stats_i.items():
                stats[k] = safe_int(row[idx]) if idx is not None else 0

            items.append({
                "name": name,
                "ilvl": ilvl,
                "slot": slot,
                "stats": stats,
                "materia_slots": 2  # default, can be updated later
            })
        except Exception as e:
            log(f"Row {i} ERROR: {e}")
            continue

    f.close()
    log(f"Total items parsed: {len(items)}")
    log(f"TOTAL TIME: {round(time.time() - start_time, 2)}s")
    return items


def load_all_items():
    # path can be dynamic if needed
    items = parse_items()
    if not items:
        log("No items loaded")
        return [], 0
    max_ilvl = max(i["ilvl"] for i in items)
    return items, max_ilvl
