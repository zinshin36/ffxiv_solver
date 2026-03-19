import csv
import os
from engine.logger import log
from engine.runtime_paths import GAME_DATA_DIR

# -------------------------
# SLOT MAP & FILTERS
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

INVALID_SLOTS = {0, 6, 13, 14, 15, 16, 17, 18, 19, 20, 24}

# -------------------------
# SAFE UTILITIES
# -------------------------
def safe_int(v):
    try:
        return int(v)
    except:
        try:
            return int(float(v))
        except:
            return 0

def find_column(header, keywords, required=True):
    header_lower = [h.lower() for h in header]
    for key in keywords:
        for i, col in enumerate(header_lower):
            if key in col:
                return i
    if required:
        raise Exception(f"Column not found: {keywords}")
    return None

# -------------------------
# LOAD BASE PARAMS
# -------------------------
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
                key = safe_int(row[0])
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

# -------------------------
# LOAD JOBS (BLM FILTER)
# -------------------------
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
                key = safe_int(row[0])
                jobs[key] = row[blm_i].strip() in ["1", "true", "True"]
            except:
                continue
    return jobs

# -------------------------
# WEAPON DETECTION
# -------------------------
def detect_weapon(name, row, header):
    name_l = name.lower()
    if any(x in name_l for x in ["rod", "staff", "cane", "wand", "scepter"]):
        return True
    ui_idx = find_column(header, ["itemuicategory"], required=False)
    if ui_idx is not None:
        val = row[ui_idx]
        if val and val.isdigit() and int(val) < 100:
            return True
    return False

# -------------------------
# LOAD ITEMS
# -------------------------
def load_items(min_ilvl=0):
    log("[PARSER] Loading Item.csv...")
    base_params = load_base_params()
    jobs = load_jobs()
    path = os.path.join(GAME_DATA_DIR, "Item.csv")
    items = []
    max_ilvl = 0
    with open(path, encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        # column detection (robust for both CSV formats)
        name_i = find_column(header, ["name"])
        ilvl_i = find_column(header, ["levelitem", "itemlevel"])
        slot_i = find_column(header, ["equipslotcategory"])
        job_i = find_column(header, ["classjobcategory"])
        materia_i = find_column(header, ["materiaslotcount"], required=False)
        param_indices = [i for i, c in enumerate(header) if "baseparam[" in c.lower()]
        value_indices = [i for i, c in enumerate(header) if "baseparamvalue[" in c.lower()]
        for row in reader:
            try:
                ilvl = safe_int(row[ilvl_i])
                max_ilvl = max(max_ilvl, ilvl)
                if not jobs.get(safe_int(row[job_i]), False):
                    continue
                if ilvl < min_ilvl:
                    continue
                name = row[name_i]
                slot_key = safe_int(row[slot_i])
                # SLOT LOGIC
                if slot_key in INVALID_SLOTS:
                    slot = "weapon" if detect_weapon(name, row, header) else None
                else:
                    slot = SLOT_FIX.get(slot_key) or ("weapon" if detect_weapon(name, row, header) else None)
                if not slot:
                    continue
                # STATS
                stats = {"crit": 0, "dh": 0, "det": 0, "sps": 0, "int": 0}
                for p_i, v_i in zip(param_indices, value_indices):
                    try:
                        stat = base_params.get(safe_int(row[p_i]))
                        if stat:
                            stats[stat] += safe_int(row[v_i])
                    except:
                        continue
                # MATERIA SLOTS
                materia_slots = safe_int(row[materia_i]) if materia_i is not None else 0
                items.append({
                    "name": name,
                    "ilvl": ilvl,
                    "slot": slot,
                    "stats": stats,
                    "materia_slots": materia_slots
                })
            except:
                continue
    log(f"[PARSER] Max iLvl: {max_ilvl}")
    log(f"[PARSER] Items after filter: {len(items)}")
    return items

# -------------------------
# LOAD MATERIA
# -------------------------
def load_materia():
    path = os.path.join(GAME_DATA_DIR, "Materia.csv")
    materia_list = []
    with open(path, encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            try:
                materia_list.append({
                    "id": safe_int(row[0]),
                    "item": [safe_int(v) for v in row[1:17]],
                    "base_param": safe_int(row[17]),
                    "values": [safe_int(v) for v in row[18:34]]
                })
            except:
                continue
    log(f"[PARSER] Materia parsed ({len(materia_list)})")
    return materia_list
