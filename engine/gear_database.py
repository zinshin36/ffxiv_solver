from engine.csv_loader import load_csv, i
from engine.logger import log

BLM_COLUMN = 26


def load_base_params():

    rows = load_csv("BaseParam.csv")
    mapping = {}

    for r in rows[1:]:
        mapping[r[0]] = r[1]

    return mapping


def load_classjobs():

    rows = load_csv("ClassJobCategory.csv")
    jobs = {}

    for r in rows[1:]:
        jobs[r[0]] = r

    return jobs


def load_items(min_ilvl):

    base_params = load_base_params()
    jobs = load_classjobs()

    rows = load_csv("Item.csv")

    items = []

    for r in rows[1:]:

        name = r[1]
        ilvl = i(r[10])
        jobcat = r[2]

        if not name:
            continue

        if ilvl < min_ilvl:
            continue

        jobrow = jobs.get(jobcat)

        if not jobrow:
            continue

        if jobrow[BLM_COLUMN] != "True":
            continue

        stats = {
            "Intelligence": i(r[40]),
            "CriticalHit": i(r[50]),
            "Determination": i(r[51]),
            "DirectHitRate": i(r[52]),
            "SpellSpeed": i(r[53])
        }

        item = {
            "name": name,
            "slot": r[4],
            "ilvl": ilvl,
            "materia_slots": i(r[30]),
            "stats": stats
        }

        items.append(item)

    log(f"Items parsed ({len(items)})")

    return items
