from engine.csv_loader import load_csv, to_int
from engine.logger import log


STAT_MAP = {
    "Critical Hit": "CriticalHit",
    "Determination": "Determination",
    "Direct Hit Rate": "DirectHitRate",
    "Spell Speed": "SpellSpeed",
    "Intelligence": "Intelligence"
}


def find_column(header, text):

    text = text.lower()

    for i, col in enumerate(header):

        if text in col.lower():
            return i

    raise Exception(f"Column containing '{text}' not found")


def find_baseparam_pairs(header):

    pairs = []

    for i, col in enumerate(header):

        if col.startswith("BaseParam["):

            pairs.append((i, i + 1))

    return pairs


def parse_stats(row, stat_pairs):

    stats = {}

    for stat_col, value_col in stat_pairs:

        if stat_col >= len(row) or value_col >= len(row):
            continue

        stat_name = row[stat_col]

        if not stat_name:
            continue

        mapped = STAT_MAP.get(stat_name)

        if not mapped:
            continue

        stats[mapped] = to_int(row[value_col])

    return stats


def load_all_items():

    rows = load_csv("Item.csv")

    header = rows[1]

    name_col = find_column(header, "Name")
    ilvl_col = find_column(header, "Level")
    job_col = find_column(header, "ClassJobCategory")
    slot_col = find_column(header, "EquipSlotCategory")
    materia_col = find_column(header, "MateriaSlotCount")

    stat_pairs = find_baseparam_pairs(header)

    log(f"Stat pairs detected: {len(stat_pairs)}")

    items = []

    max_ilvl = 0

    for r in rows[3:]:

        if len(r) <= ilvl_col:
            continue

        name = r[name_col]
        ilvl = to_int(r[ilvl_col])
        jobs = r[job_col]
        slot = r[slot_col]
        materia_slots = to_int(r[materia_col])

        if not name:
            continue

        if jobs and "BLM" not in jobs and "THM" not in jobs:
            continue

        stats = parse_stats(r, stat_pairs)

        item = {
            "name": name,
            "slot": slot,
            "ilvl": ilvl,
            "materia_slots": materia_slots,
            "stats": stats
        }

        items.append(item)

        if ilvl > max_ilvl:
            max_ilvl = ilvl

    log(f"Items parsed ({len(items)})")
    log(f"Highest item level detected: {max_ilvl}")

    return items, max_ilvl


def filter_items(items, min_ilvl):

    filtered = [i for i in items if i["ilvl"] >= min_ilvl]

    log(f"Items after ilvl filter ({len(filtered)}) min_ilvl={min_ilvl}")

    return filtered
