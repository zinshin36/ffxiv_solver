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


# -----------------------------
# BASE PARAMS (stats mapping)
# -----------------------------
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
                elif "direct hit" in name:
                    params[key] = "dh"
                elif "determination" in name:
                    params[key] = "det"
                elif "spell speed" in name:
                    params[key] = "sps"
                elif "intelligence" in name:
                    params[key] = "int"
            except:
                continue

    log(f"[PARSER] Base params: {len(params)}")
    return params


# -----------------------------
# SLOT MAPPING (CRITICAL FIX)
# -----------------------------
def load_equip_slots():
    path = os.path.join(GAME_DATA_DIR, "EquipSlotCategory.csv")
    slots = {}

    with open(path, encoding="utf-8") as f:
        reader = csv.reader(f)

        next(reader)
        header = next(reader)
        next(reader)

        for row in reader:
            try:
                key = int(row[0])

                for i in range(1, len(row)):
                    if row[i] == "1":
                        col = header[i].lower()

                        mapping = {
                            "mainhand": "weapon",
                            "offhand": "offhand",
                            "head": "head",
                            "body": "body",
                            "gloves": "hands",
                            "legs": "legs",
                            "feet": "feet",
                            "ears": "earrings",
                            "neck": "necklace",
                            "wrists": "bracelet",
                            "fingerl": "ring",
                            "fingerr": "ring"
                        }

                        if col in mapping:
                            slots[key] = mapping[col]

            except:
                continue

    log(f"[PARSER] Slot mappings: {len(slots)}")
    return slots


# -----------------------------
# JOB FILTER (BLM)
# -----------------------------
def load_jobs():
    path = os.path.join(GAME_DATA_DIR, "ClassJobCategory.csv")
    jobs = {}

    with open(path, encoding="utf-8") as f:
        reader = csv.reader(f)

        next(reader)
        header = next(reader)
        next(reader)

        blm_index = find_column(header, ["blm", "black"])

        for row in reader:
            try:
                key = int(row[0])
                val = row[blm_index].strip().lower()
                jobs[key] = val in ["true", "1"]
            except:
                continue

    log(f"[PARSER] Job table loaded")
    return jobs


# -----------------------------
# MAIN ITEM LOADER
# -----------------------------
def load_items(min_ilvl=None):
    log("Loading Item.csv...")

    base_params = load_base_params()
    slots = load_equip_slots()
    jobs = load_jobs()

    path = os.path.join(GAME_DATA_DIR, "Item.csv")

    items = []
    max_ilvl = 0

    with open(path, encoding="utf-8") as f:
        reader = csv.reader(f)

        header = next(reader)

        name_i = find_column(header, ["name", "singular"])
        ilvl_i = find_column(header, ["levelitem"])
        slot_i = find_column(header, ["equipslotcategory"])
        job_i = find_column(header, ["classjobcategory"])
        materia_i = find_column(header, ["materiaslotcount"])

        param_indices = [i for i, c in enumerate(header) if "baseparam[" in c.lower()]
        value_indices = [i for i, c in enumerate(header) if "baseparamvalue[" in c.lower()]

        log(f"[PARSER] Columns OK")

        for row_i, row in enumerate(reader):

            if row_i % 5000 == 0:
                log(f"[PARSER] Row {row_i}")

            try:
                ilvl = int(row[ilvl_i])
                max_ilvl = max(max_ilvl, ilvl)

                if min_ilvl and ilvl < min_ilvl:
                    continue

                if not jobs.get(int(row[job_i]), False):
                    continue

                slot = slots.get(int(row[slot_i]))
                if not slot or slot == "offhand":
                    continue

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

            except Exception as e:
                log(f"[PARSER ERROR] Row {row_i}: {e}")

    log(f"[PARSER] Loaded {len(items)} usable items (max ilvl: {max_ilvl})")
    return items, max_ilvl
