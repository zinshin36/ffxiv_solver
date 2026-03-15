from engine.csv_loader import load_csv, to_int
from engine.logger import log


def find_blm_column():

    rows = load_csv("ClassJobCategory.csv")

    header = rows[0]

    for i, col in enumerate(header):

        if "BlackMage" in col or "BLM" in col:
            return i

    log("BLM column not found, defaulting to 26")

    return 26


def load_class_jobs():

    rows = load_csv("ClassJobCategory.csv")

    mapping = {}

    for r in rows[1:]:
        mapping[r[0]] = r

    return rows, mapping


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

    rows_jobs, job_map = load_class_jobs()
    caps = load_item_caps()

    blm_column = find_blm_column()

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

        if blm_column >= len(jobrow):
            continue

        if jobrow[blm_column] != "True":
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
