from engine.csv_loader import load_csv, to_int
from engine.logger import log


STAT_MAP = {
    "Critical Hit": "CriticalHit",
    "Determination": "Determination",
    "Direct Hit Rate": "DirectHitRate",
    "Spell Speed": "SpellSpeed",
    "Intelligence": "Intelligence"
}


def parse_stats(row):

    stats = {}

    # BaseParam pairs start at column 60
    for i in range(60, 72, 2):

        stat_name = row[i]
        value = row[i + 1]

        if not stat_name:
            continue

        mapped = STAT_MAP.get(stat_name)

        if not mapped:
            continue

        stats[mapped] = to_int(value)

    return stats


def load_items(min_ilvl):

    rows = load_csv("Item.csv")

    items = []

    # skip 3 header rows
    for r in rows[3:]:

        name = r[10]
        ilvl = to_int(r[12])
        jobs = r[44]
        slot = r[18]
        materia_slots = to_int(r[87])

        if not name:
            continue

        if ilvl < min_ilvl:
            continue

        # check if BLM usable
        if "BLM" not in jobs and "THM" not in jobs:
            continue

        stats = parse_stats(r)

        item = {
            "name": name,
            "slot": slot,
            "ilvl": ilvl,
            "materia_slots": materia_slots,
            "stats": stats
        }

        items.append(item)

    log(f"Items parsed ({len(items)})")

    return items
