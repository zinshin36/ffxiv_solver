from engine.csv_loader import load_csv, to_int
from engine.logger import log


STAT_MAP = {
    "Critical Hit": "crit",
    "Determination": "det",
    "Direct Hit Rate": "dh",
    "Spell Speed": "sps",
    "Intelligence": "int"
}


def build_itemlevel_table():

    rows = load_csv("ItemLevel.csv")

    header = rows[1]

    key_col = header.index("key")
    ilvl_col = None

    for i, c in enumerate(header):
        if "ItemLevel" in c or "Level" in c:
            ilvl_col = i
            break

    table = {}

    for r in rows[3:]:

        key = to_int(r[key_col])

        if key == 0:
            continue

        table[key] = to_int(r[ilvl_col])

    return table


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

        stat_name = row[stat_col]

        if stat_name not in STAT_MAP:
            continue

        stats[STAT_MAP[stat_name]] = to_int(row[val_col])

    return stats


def load_all_items():

    ilvl_table = build_itemlevel_table()

    rows = load_csv("Item.csv")
    header = rows[1]

    name_col = header.index("Name")
    ilvl_key_col = header.index("LevelItem")
    slot_col = header.index("EquipSlotCategory")
    materia_col = header.index("MateriaSlotCount")

    stat_pairs = find_stat_pairs(header)

    items = []
    max_ilvl = 0

    for r in rows[3:]:

        name = r[name_col]

        if not name:
            continue

        level_key = to_int(r[ilvl_key_col])

        if level_key not in ilvl_table:
            continue

        ilvl = ilvl_table[level_key]

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
