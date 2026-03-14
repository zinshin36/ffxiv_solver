from engine.csv_loader import read_csv, safe_int
from engine.logger import log

BLM_JOB_COLUMN = 26  # column index for Black Mage in ClassJobCategory


def load_base_params():
    rows = read_csv("BaseParam.csv")
    mapping = {}

    for r in rows[1:]:
        mapping[r[0]] = r[1]

    return mapping


def load_classjob():
    rows = read_csv("ClassJobCategory.csv")
    mapping = {}

    for r in rows[1:]:
        mapping[r[0]] = r

    return mapping


def load_items(min_ilvl=0):
    base_params = load_base_params()
    job_map = load_classjob()

    rows = read_csv("Item.csv")

    items = []

    for r in rows[1:]:

        name = r[1]
        ilvl = safe_int(r[10])
        job_cat = r[2]

        if not name or ilvl < min_ilvl:
            continue

        job_row = job_map.get(job_cat)

        if not job_row:
            continue

        if job_row[BLM_JOB_COLUMN] != "True":
            continue

        stats = {
            "Intelligence": safe_int(r[40]),
            "CriticalHit": safe_int(r[50]),
            "Determination": safe_int(r[51]),
            "DirectHitRate": safe_int(r[52]),
            "SpellSpeed": safe_int(r[53]),
        }

        item = {
            "Name": name,
            "slot": r[4],
            "ilvl": ilvl,
            "MateriaSlots": safe_int(r[30]),
            "stats": stats
        }

        items.append(item)

    log(f"BLM items loaded: {len(items)}")

    return items
