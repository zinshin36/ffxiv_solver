import csv
import time
from engine.logger import log


def safe_int(val):
    try:
        return int(val)
    except:
        return 0


def parse_items(path):

    log("STEP 1: entering parse_items")
    start_time = time.time()

    items = []

    # --- STEP 2: open file ---
    log("STEP 2: opening file")
    f = open(path, encoding="utf-8", newline="")
    log("STEP 2 DONE: file opened")

    # --- STEP 3: create reader ---
    log("STEP 3: creating csv reader")
    reader = csv.reader(f)
    log("STEP 3 DONE: reader created")

    # --- STEP 4: read headers ---
    log("STEP 4: reading headers")
    headers = next(reader)
    log(f"STEP 4 DONE: headers read ({len(headers)} columns)")

    # --- STEP 5: basic column detection ---
    log("STEP 5: detecting columns")

    def find_idx(keys):
        for i, h in enumerate(headers):
            hl = h.lower()
            if any(k in hl for k in keys):
                return i
        return None

    name_i = find_idx(["name"])
    ilvl_i = find_idx(["levelitem", "itemlevel"])
    slot_i = find_idx(["equipslotcategory"])

    log(f"STEP 5 DONE: name={name_i}, ilvl={ilvl_i}, slot={slot_i}")

    # --- STEP 6: test first 10 rows ONLY ---
    log("STEP 6: testing first 10 rows")

    for i in range(10):
        try:
            row = next(reader)
            log(f"Row {i} OK len={len(row)}")
        except StopIteration:
            log("File ended early")
            break
        except Exception as e:
            log(f"Row {i} ERROR: {e}")
            break

    log("STEP 6 DONE")

    # --- STEP 7: full loop with watchdog ---
    log("STEP 7: starting full parse loop")

    last_log = time.time()

    for i, row in enumerate(reader):

        # 🔥 watchdog: if loop freezes, we see last count
        if i % 1000 == 0:
            now = time.time()
            log(f"Loop alive at row {i} (+{round(now - last_log, 2)}s)")
            last_log = now

        # minimal work (no filters yet)
        try:
            _ = row[name_i]
            _ = row[ilvl_i]
            _ = row[slot_i]
        except Exception as e:
            log(f"Row {i} access error: {e}")
            continue

        items.append(1)  # dummy

    log(f"STEP 7 DONE: total rows {len(items)}")

    f.close()

    log(f"TOTAL TIME: {round(time.time() - start_time, 2)}s")

    return []
    

def load_all_items(path):
    return parse_items(path)
