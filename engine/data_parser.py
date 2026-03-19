import csv
import os
from engine.logger import log
from engine.runtime_paths import GAME_DATA_DIR


# -------------------------
# SLOT MAP (PARTIAL)
# -------------------------
SLOT_FIX = {
    3: "head",
    4: "body",
    5: "hands",
    7: "legs",
    8: "feet",
    9: "earrings",
    10: "necklace",
    11: "bracelet",
    12: "ring",
}

# invalid / ignore
INVALID_SLOTS = {0, 6, 13, 14, 15, 16, 17, 18, 19, 20, 24}


def find_column(header, keywords):
    header_lower = [h.lower() for h in header]

    for key in keywords:
        for i, col in enumerate(header_lower):
            if key in col:
                return i

    raise Exception(f"Column not found: {keywords}")


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

    return jobs


def detect_weapon(name, row, header):
    """
    Fallback weapon detection (VERY IMPORTANT)
    """

    name_l = name.lower()

    # BLM weapons
    if any(x in name_l for x in [
        "rod", "staff", "cane", "scepter", "wand"
    ]):
        return True

    # backup: check UI category if exists
    try:
        ui_idx = find_column(header, ["itemuicategory"])
        ui_val = row[ui_idx]

        # known weapon categories often < 100
        if ui_val and ui_val.isdigit():
            if int(ui_val) < 100:
                return True
    except:
        pass

    return False


def load_items(min_ilvl=0):

    log("Loading Item.csv...")

    base_params = load_base_params()
    jobs = load_jobs()

    path = os.path.join(GAME_DATA_DIR, "Item.csv")

    items = []
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

        for row in reader:
            try:
                ilvl = int(row[ilvl_i])
                max_ilvl = max(max_ilvl, ilvl)

                if not jobs.get(int(row[job_i]), False):
                    continue

                if ilvl < min_ilvl:
                    continue

                name = row[name_i]
                slot_key = int(row[slot_i])

                # -------------------------
                # SLOT DETECTION
                # -------------------------
                if slot_key in INVALID_SLOTS:
                    # try weapon fallback
                    if detect_weapon(name, row, header):
                        slot = "weapon"
                    else:
                        continue
                else:
                    slot = SLOT_FIX.get(slot_key)

                    if not slot:
                        # fallback weapon detection
                        if detect_weapon(name, row, header):
                            slot = "weapon"
                        else:
                            continue

                # -------------------------
                # STATS
                # -------------------------
                stats = {"crit": 0, "dh": 0, "det": 0, "sps": 0, "int": 0}

                for p_i, v_i in zip(param_indices, value_indices):
                    try:
                        stat = base_params.get(int(row[p_i]))
                        if stat:
                            stats[stat] += int(row[v_i])
                    except:
                        continue

                items.append({
                    "name": name,
                    "ilvl": ilvl,
                    "slot": slot,
                    "stats": stats,
                    "materia_slots": int(row[materia_i])
                })

            except:
                continue

    log(f"[PARSER] Max iLvl: {max_ilvl}")
    log(f"[PARSER] Items after filter: {len(items)}")

    return items, max_ilvl
