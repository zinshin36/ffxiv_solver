import csv
import os
from engine.logger import log
from engine.runtime_paths import GAME_DATA_DIR


def find_column(header, keywords):
    header_lower = [h.lower() for h in header]

    for key in keywords:
        for i, col in enumerate(header_lower):
            if key in col:
                return i

    log(f"[COLUMN ERROR] Could not find column for {keywords}")
    for i, col in enumerate(header):
        log(f"[HEADER] {i}: {col}")

    raise Exception(f"Column not found: {keywords}")


# =========================
# BASE PARAMS
# =========================
def load_base_params():
    path = os.path.join(GAME_DATA_DIR, "BaseParam.csv")
    params = {}

    with open(path, encoding="utf-8") as f:
        reader = csv.reader(f)

        next(reader)
        header = next(reader)
        next(reader)

        name_i = find_column(header, ["name"])

        for row in reader:
            try:
                key = int(row[0])
                name = row[name_i].lower()

                if "critical" in name:
                    params[key] = "crit"
                elif "direct" in name:
                    params[key] = "dh"
                elif "determination" in name:
                    params[key] = "det"
                elif "spell" in name:
                    params[key] = "sps"
                elif "intelligence" in name:
                    params[key] = "int"
            except:
                continue

    log(f"[PARSER] Base params: {len(params)}")
    return params


# =========================
# SLOT MAPPING (FIXED)
# =========================
def load_equip_slots():
    path = os.path.join(GAME_DATA_DIR, "EquipSlotCategory.csv")
    slots = {}

    with open(path, encoding="utf-8") as f:
        reader = csv.reader(f)

        next(reader)
        header = next(reader)
        next(reader)

        log(f"[PARSER] EquipSlot headers loaded")

        for row in reader:
            try:
                key = int(row[0])
                detected = None

                for i in range(1, len(row)):
                    if row[i] == "1":
                        col = header[i].lower()

                        if "main" in col:
                            detected = "weapon"
                        elif "off" in col:
                            detected = "offhand"
                        elif "head" in col:
                            detected = "head"
                        elif "body" in col:
                            detected = "body"
                        elif "hand" in col or "glove" in col:
                            detected = "hands"
                        elif "leg" in col:
                            detected = "legs"
                        elif "foot" in col:
                            detected = "feet"
                        elif "ear" in col:
                            detected = "earrings"
                        elif "neck" in col:
                            detected = "necklace"
                        elif "wrist" in col:
                            detected = "bracelet"
                        elif "finger" in col or "ring" in col:
                            detected = "ring"

                if detected:
                    slots[key] = detected
                else:
                    log(f"[SLOT WARNING] Unknown slot key={key}")

            except Exception as e:
                log(f"[SLOT ERROR] {e}")

    log(f"[PARSER] Slot mappings: {len(slots)}")
    return slots


# =========================
# JOB FILTER
# =========================
def load_jobs():
    path = os.path.join(GAME_DATA_DIR, "ClassJobCategory.csv")
    jobs = {}

    with open(path, encoding="utf-8") as f:
        reader = csv.reader(f)

        next(reader)
        header = next(reader)
        next(reader)

        blm_i = find_column(header, ["blm", "black"])

        for row in reader:
            try:
                key = int(row[0])
                jobs[key] = row[blm_i].strip() in ["1", "true", "True"]
            except:
                continue

    log("[PARSER] Job table loaded")
    return jobs


# =========================
# MAIN LOADER
# =========================
def load_items(min_ilvl=0):

    log("Loading Item.csv...")

    base_params = load_base_params()
    slots = load_equip_slots()
    jobs = load_jobs()

    path = os.path.join(GAME_DATA_DIR, "Item.csv")

    items = []
    total_rows = 0
    blm_items = 0
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

                if not jobs.get(int(row[job_i]), False):
                    continue

                blm_items += 1

                if ilvl < min_ilvl:
                    continue

                slot_key = int(row[slot_i])
                slot = slots.get(slot_key, "unknown")

                if slot == "unknown":
                    log(f"[SLOT MISS] {row[name_i]} (key={slot_key})")

                stats = {"crit": 0, "dh": 0, "det": 0, "sps": 0, "int": 0}

                for p_i, v_i in zip(param_indices, value_indices):
                    try:
                        stat = base_params.get(int(row[p_i]))
                        if stat:
                            stats[stat] += int(row[v_i])
                    except:
                        continue

                items.append({
                    "name": row[name_i],
                    "ilvl": ilvl,
                    "slot": slot,
                    "stats": stats,
                    "materia_slots": int(row[materia_i])
                })

            except:
                continue

    log(f"[PARSER] TOTAL rows: {total_rows}")
    log(f"[PARSER] BLM-capable items: {blm_items}")
    log(f"[PARSER] Max iLvl: {max_ilvl}")
    log(f"[PARSER] After min iLvl filter: {len(items)}")

    return items
