from engine.csv_loader import load_csv, to_int
from engine.logger import log


def normalize(s):

    if not s:
        return ""

    return s.lower().replace(" ", "").replace("_", "")


def safe_get(row, idx):

    if idx is None:
        return ""

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


# -------------------------
# BUILD ITEMLEVEL TABLE
# -------------------------

def build_itemlevel_table():

    rows = load_csv("ItemLevel.csv")

    header = rows[1]

    key_col = detect_column(header, ["key"])
    ilvl_col = detect_column(header, ["itemlevel", "level"])

    table = {}

    for r in rows[3:]:

        key = to_int(safe_get(r, key_col))
        ilvl = to_int(safe_get(r, ilvl_col))

        if key <= 0:
            continue

        table[key] = ilvl

    log(f"ItemLevel table built ({len(table)})")

    return table


# -------------------------
# STAT PAIRS
# -------------------------

def discover_stat_pairs(header):

    pairs = []

    for i, col in enumerate(header):

        if col.startswith("BaseParam["):
            pairs.append((i, i + 1))

    log(f"Stat pairs detected: {len(pairs)}")

    return pairs


# -------------------------
# PARSE STATS
# -------------------------

def parse_stats(row, stat_pairs):

    stats = {}

    for stat_col, val_col in stat_pairs:

        stat_name = normalize(safe_get(row, stat_col))

        if not stat_name:
            continue

        val = to_int(safe_get(row, val_col))

        if val <= 0:
            continue

        stats[stat_name] = val

    return stats


# -------------------------
# LOAD ALL ITEMS
# -------------------------

def load_all_items():

    itemlevel_table = build_itemlevel_table()

    rows = load_csv("Item.csv")

    header = rows[1]

    name_col = detect_column(header, ["name", "singular"])
    slot_col = detect_column(header, ["equipslot"])
    materia_col = detect_column(header, ["materiaslotcount"])
    level_key_col = detect_column(header, ["levelitem", "level{item}", "level"])

    stat_pairs = discover_stat_pairs(header)

    items = []
    max_ilvl = 0

    for r in rows[3:]:

        name = safe_get(r, name_col)

        if name == "":
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


# -------------------------
# FILTER BY ILVL
# -------------------------

def filter_items(items, min_ilvl):

    filtered = []

    for i in items:

        ilvl = to_int(i.get("ilvl"))

        if ilvl >= min_ilvl:
            filtered.append(i)

    log(f"Items after ilvl filter ({len(filtered)})")

    return filtered
