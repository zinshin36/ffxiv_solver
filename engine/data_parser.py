import csv
import os
from engine.logger import log
from engine.runtime_paths import GAME_DATA_DIR


def load_base_params():
    path = os.path.join(GAME_DATA_DIR, "BaseParam.csv")
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


def load_equip_slots():
    path = os.path.join(GAME_DATA_DIR, "EquipSlotCategory.csv")
    slots = {}

    with open(path, encoding="utf-8") as f:
        reader = csv.reader(f)

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

    log(f"Loaded {len(slots)} slot mappings")
    return slots


def detect_blm_column(header):
    """
    Try to find BLM column dynamically
    """
    for i, col in enumerate(header):
        name = col.lower()

        if "black" in name or "blm" in name:
            return i

    raise Exception("Could not find Black Mage column in ClassJobCategory.csv")


def load_jobs():
    path = os.path.join(GAME_DATA_DIR, "ClassJobCategory.csv")
    jobs = {}

    with open(path, encoding="utf-8") as f:
        reader = csv.reader(f)

        header = next(reader)

        blm_index = detect_blm_column(header)
        log(f"Detected BLM column: {header[blm_index]}")

        next(reader)

        for row in reader:
            try:
                key = int(row[0])

                val = row[blm_index].strip().lower()

                jobs[key] = val in ["true", "1"]
            except:
                continue

    log("Loaded job categories")
    return jobs


def load_items():
    log("Loading Item.csv...")

    base_params = load_base_params()
    slots = load_equip_slots()
    jobs = load_jobs()

    path = os.path.join(GAME_DATA_DIR, "Item.csv")

    items = []

    with open(path, encoding="utf-8") as f:
        reader = csv.reader(f)

        header = next(reader)
        next(reader)

        name_i = header.index("Name")
        ilvl_i = header.index("Level{Item}")
        slot_i = header.index("EquipSlotCategory")
        job_i = header.index("ClassJobCategory")

        param_indices = [i for i, c in enumerate(header) if "BaseParam" in c]
        value_indices = [i for i, c in enumerate(header) if "BaseParamValue" in c]

        for row in reader:
            try:
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
                    "ilvl": int(row[ilvl_i]),
                    "slot": slot,
                    "stats": stats,
                    "materia_slots": 2
                })

            except:
                continue

    log(f"Loaded {len(items)} BLM items")
    return items
