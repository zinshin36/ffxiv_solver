from engine.csv_loader import load_csv, to_int
from engine.logger import log


STAT_NAMES = {
    "criticalhit": "crit",
    "determination": "det",
    "directhit": "dh",
    "spellspeed": "sps",
    "intelligence": "int"
}


def normalize(t):
    return t.lower().replace(" ", "").replace("_", "")


def safe_get(row, idx):

    if idx >= len(row):
        return ""

    return row[idx]


def detect_column(header, keywords):

    header_norm = [normalize(h) for h in header]

    for i, col in enumerate(header_norm):

        for k in keywords:

            if k in col:
                return i

    return None


def build_itemlevel_table():

    rows = load_csv("ItemLevel.csv")

    header = rows[1]

    key_col = detect_column(header, ["key"])

    ilvl_col = detect_column(header, ["itemlevel", "level"])

    table = {}

    for r in rows[3:]:

        key = to_int(safe_get(r, key_col))

        if key == 0:
            continue

        table[key] = to_int(safe_get(r, ilvl_col))

    log(f"ItemLevel table built ({len(table)})")

    return table


def discover_stat_pairs(header):

    pairs = []

    for i, col in enumerate(header):

        if col.startswith("BaseParam["):
            pairs.append((i, i + 1))

    log(f"Stat pairs detected: {len(pairs)}")

    return pairs


def parse_stats(row, stat_pairs):

    stats = {}

    for stat_col, val_col in stat_pairs:

        stat = normalize(safe_get(row, stat_col))

        if not stat:
            continue

        for k in STAT_NAMES:

            if k in stat:
                stats[STAT_NAMES[k]] = to_int(safe_get(row, val_col))

    return stats


def load_all_items():

    itemlevel_table = build_itemlevel_table()

    rows = load_csv("Item.csv")

    header = rows[1]

    name_col = detect_column(header, ["name", "singular"])
    slot_col = detect_column(header, ["equipslot"])
    materia_col = detect_column(header, ["materiaslotcount"])
    level_key_col = detect_column(header, ["levelitem", "level{item}"])

    if level_key_col is None:
        level_key_col = detect_column(header, ["level"])

    stat_pairs = discover_stat_pairs(header)

    items = []
    max_ilvl = 0

    for r in rows[3:]:

        name = safe_get(r, name_col)

        if not name:
            continue

        level_key = to_int(safe_get(r, level_key_col))

        ilvl = itemlevel_table.get(level_key, 0)

        slot = safe_get(r, slot_col)

        materia_slots = to_int(safe_get(r, materia_col))

        stats = parse_stats(r, stat_pairs)

        item = {
            "name": name,
            "slot": slot,
            "materia_slots": materia_slots,
            "ilvl": ilvl,
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

    log(f"Items after ilvl filter ({len(filtered)})")

    return filtered
