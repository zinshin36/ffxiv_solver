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

    log("HEADER DUMP:")
    for i, col in enumerate(header):
        log(f"{i}: {col}")

    raise Exception(f"Column not found for {keywords}")


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

    log(f"Loaded {len(params)} base params")
    return params


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

    log(f"Loaded {len(slots)} slot mappings")
    return slots


def load_jobs():
    path = os.path.join(GAME_DATA_DIR, "ClassJobCategory.csv")
    jobs = {}

    with open(path, encoding="utf-8") as f:
        reader = csv.reader(f)

        next(reader)
        header = next(reader)
        next(reader)

        blm_index = find_column(header, ["blm", "black"])
        log(f"BLM column: {header[blm_index]}")

        for row in reader:
            try:
                key = int(row[0])
                val = row[blm_index].strip().lower()
                jobs[key] = val in ["true", "1"]
            except:
                continue

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

        # ✅ THIS IS THE FIX
        header = next(reader)

        name_i = find_column(header, ["name"])
        ilvl_i = find_column(header, ["levelitem"])
        slot_i = find_column(header, ["equipslotcategory"])
        job_i = find_column(header, ["classjobcategory"])

        param_indices = [i for i, c in enumerate(header) if "baseparam[" in c.lower()]
        value_indices = [i for i, c in enumerate(header) if "baseparamvalue[" in c.lower()]

        log(f"Detected columns: name={name_i}, ilvl={ilvl_i}, slot={slot_i}")

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
                    "materia_slots": int(row[find_column(header, ["materiaslotcount"])])
                })

            except:
                continue

    log(f"Loaded {len(items)} BLM items")
    return items
