from engine.csv_loader import load_csv, find_col, to_int
from engine.logger import log


STAT_MAP = {
    "Critical Hit": "crit",
    "Determination": "det",
    "Direct Hit Rate": "dh",
    "Spell Speed": "sps",
    "Intelligence": "int"
}


def find_stat_pairs(header):

    pairs = []

    for i, col in enumerate(header):

        if col.startswith("BaseParam["):
            pairs.append((i, i + 1))

    return pairs


def parse_stats(row, pairs):

    stats = {}

    for stat_col, val_col in pairs:

        if stat_col >= len(row):
            continue

        stat = row[stat_col]

        if stat not in STAT_MAP:
            continue

        stats[STAT_MAP[stat]] = to_int(row[val_col])

    return stats


def load_all_items():

    rows = load_csv("Item.csv")

    header = rows[1]

    name_col = find_col(header, "Name")
    ilvl_col = find_col(header, "LevelItem")
    slot_col = find_col(header, "EquipSlotCategory")
    materia_col = find_col(header, "MateriaSlotCount")

    stat_pairs = find_stat_pairs(header)

    items = []
    max_ilvl = 0

    for r in rows[3:]:

        if len(r) <= name_col:
            continue

        name = r[name_col]

        if not name:
            continue

        ilvl = to_int(r[ilvl_col])

        stats = parse_stats(r, stat_pairs)

        item = {
            "name": name,
            "slot": r[slot_col],
            "ilvl": ilvl,
            "materia_slots": to_int(r[materia_col]),
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
