import csv
import time
from engine.logger import log


def safe_int(val):
    """Convert value to int, return 0 if fails."""
    try:
        if val is None or val == "":
            return 0
        return int(float(val))
    except:
        return 0


def normalize_header(h):
    """Lowercase and remove spaces/underscores for matching."""
    return h.lower().replace("_", "").replace(" ", "")


def load_all_items():
    """Load all items from Item.csv in game_data folder."""
    path = "game_data/Item.csv"
    log(f"STEP 1: opening file {path}")

    start_time = time.time()

    with open(path, encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        headers = next(reader)

        # Detect columns
        header_map = {}
        for i, h in enumerate(headers):
            h_norm = normalize_header(h)
            if "name" in h_norm:
                header_map["name"] = i
            elif "itemlevel" in h_norm or "levelitem" in h_norm:
                header_map["ilvl"] = i
            elif "slot" in h_norm or "equipslotcategory" in h_norm:
                header_map["slot"] = i
            elif "criticalhit" in h_norm:
                header_map["crit"] = i
            elif "directhit" in h_norm:
                header_map["dh"] = i
            elif "determination" in h_norm:
                header_map["det"] = i
            elif "spellspeed" in h_norm:
                header_map["sps"] = i

        log(f"Columns detected: {header_map}")

        items = []
        last_log = time.time()

        for idx, row in enumerate(reader):

            # Watchdog logging
            if idx % 5000 == 0:
                now = time.time()
                log(f"Loop alive at row {idx} (+{round(now-last_log,2)}s)")
                last_log = now

            try:
                item = {
                    "name": row[header_map.get("name", 0)],
                    "ilvl": safe_int(row[header_map.get("ilvl", 0)]),
                    "slot": row[header_map.get("slot", 0)],
                    "crit": safe_int(row[header_map.get("crit")]) if "crit" in header_map else 0,
                    "dh": safe_int(row[header_map.get("dh")]) if "dh" in header_map else 0,
                    "det": safe_int(row[header_map.get("det")]) if "det" in header_map else 0,
                    "sps": safe_int(row[header_map.get("sps")]) if "sps" in header_map else 0,
                    "materia_slots": 2  # default, can adjust later
                }
                items.append(item)
            except Exception as e:
                log(f"Row {idx} ERROR: {e}")
                continue

    log(f"Total items parsed: {len(items)}")
    log(f"TOTAL TIME: {round(time.time() - start_time,2)}s")
    return items, max(item["ilvl"] for item in items) if items else 0
