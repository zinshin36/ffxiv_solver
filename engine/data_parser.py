from engine.csv_loader import load_csv, to_int
from engine.logger import log

BLM_COLUMN = 26


def load_class_jobs():

    rows = load_csv("ClassJobCategory.csv")

    mapping = {}

    for r in rows[1:]:
        mapping[r[0]] = r

    return mapping


def load_item_caps():

    rows = load_csv("ItemLevel.csv")

    caps = {}

    for r in rows[1:]:

        ilvl = to_int(r[0])

        caps[ilvl] = {
            "CriticalHit": to_int(r[20]),
            "Determination": to_int(r[21]),
            "DirectHitRate": to_int(r[22]),
            "SpellSpeed": to_int(r[23])
        }

    return caps


def load_items(min_ilvl):

    job_map = load_class_jobs()
    caps = load_item_caps()

    rows = load_csv("Item.csv")

    items = []

    for r in rows[1:]:

        name = r[1]
        jobcat = r[2]
        slot = r[4]
        ilvl = to_int(r[10])

        if not name:
            continue

        if ilvl < min_ilvl:
            continue

        jobrow = job_map.get(jobcat)

        if not jobrow:
            continue

        if jobrow[BLM_COLUMN] != "True":
            continue

        stats = {
            "Intelligence": to_int(r[40]),
            "CriticalHit": to_int(r[50]),
            "Determination": to_int(r[51]),
            "DirectHitRate": to_int(r[52]),
            "SpellSpeed": to_int(r[53])
        }

        item = {
            "name": name,
            "slot": slot,
            "ilvl": ilvl,
            "materia_slots": to_int(r[30]),
            "cap": caps.get(ilvl, {}),
            "stats": stats
        }

        items.append(item)

    log(f"Items parsed ({len(items)})")

    return items
