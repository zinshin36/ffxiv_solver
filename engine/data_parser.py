import csv
import time


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}")


# =========================
# LOAD BASE PARAM (STAT NAMES)
# =========================
def load_base_params(path):
    params = {}

    with open(path, encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)
        next(reader)

        for row in reader:
            try:
                key = int(row[0])
                name = row[2].lower()

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

    log(f"Loaded {len(params)} base params")
    return params


# =========================
# LOAD EQUIP SLOTS
# =========================
def load_equip_slots(path):
    slots = {}

    with open(path, encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)
        header = next(reader)

        for row in reader:
            try:
                key = int(row[0])

                # find which slot is active
                for i in range(1, len(row)):
                    val = row[i]

                    if val == "1":
                        slot_name = header[i].lower()

                        if slot_name == "mainhand":
                            slots[key] = "weapon"
                        elif slot_name == "offhand":
                            slots[key] = "offhand"
                        elif slot_name == "head":
                            slots[key] = "head"
                        elif slot_name == "body":
                            slots[key] = "body"
                        elif slot_name == "gloves":
                            slots[key] = "hands"
                        elif slot_name == "legs":
                            slots[key] = "legs"
                        elif slot_name == "feet":
                            slots[key] = "feet"
                        elif slot_name == "ears":
                            slots[key] = "earrings"
                        elif slot_name == "neck":
                            slots[key] = "necklace"
                        elif slot_name == "wrists":
                            slots[key] = "bracelet"
                        elif slot_name in ["fingerl", "fingerr"]:
                            slots[key] = "ring"

            except:
                continue

    log(f"Loaded {len(slots)} slot mappings")
    return slots


# =========================
# LOAD CLASS JOB CATEGORY
# =========================
def load_jobs(path):
    jobs = {}

    with open(path, encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)

        blm_index = header.index("BLM")

        next(reader)  # types row

        for row in reader:
            try:
                key = int(row[0])
                jobs[key] = row[blm_index] == "True"
            except:
                continue

    log(f"Loaded job categories")
    return jobs


# =========================
# LOAD ITEMS
# =========================
def load_items():
    log("Loading Item.csv...")

    base_params = load_base_params("game_data/BaseParam.csv")
    slots = load_equip_slots("game_data/EquipSlotCategory.csv")
    jobs = load_jobs("game_data/ClassJobCategory.csv")

    items = []

    with open("game_data/Item.csv", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        next(reader)

        name_i = header.index("Name")
        ilvl_i = header.index("Level{Item}")
        slot_i = header.index("EquipSlotCategory")
        job_i = header.index("ClassJobCategory")

        param_indices = []
        value_indices = []

        for i, col in enumerate(header):
            if "BaseParam" in col:
                param_indices.append(i)
            if "BaseParamValue" in col:
                value_indices.append(i)

        for row in reader:
            try:
                job_cat = int(row[job_i])

                if not jobs.get(job_cat, False):
                    continue  # NOT BLM

                slot_id = int(row[slot_i])
                slot = slots.get(slot_id)

                if not slot:
                    continue

                stats = {"crit": 0, "dh": 0, "det": 0, "sps": 0, "int": 0}

                for p_i, v_i in zip(param_indices, value_indices):
                    try:
                        param = int(row[p_i])
                        value = int(row[v_i])

                        stat = base_params.get(param)
                        if stat:
                            stats[stat] += value
                    except:
                        continue

                items.append({
                    "name": row[name_i],
                    "ilvl": int(row[ilvl_i]),
                    "slot": slot,
                    "stats": stats
                })

            except:
                continue

    log(f"Loaded {len(items)} BLM items")
    return items
