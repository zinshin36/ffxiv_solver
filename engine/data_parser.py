from engine.csv_loader import load_csv, to_int
from engine.logger import log


def normalize(text):
    if not text:
        return ""
    return text.lower().replace(" ", "").replace("_", "").replace("{", "").replace("}", "")


def safe_get(row, idx):

    if idx is None:
        return ""

    if idx >= len(row):
        return ""

    return row[idx]


def detect_column(header, keywords):

    normalized = [normalize(h) for h in header]

    for i, col in enumerate(normalized):

        for k in keywords:

            if k in col:
                return i

    return None


# --------------------------------
# STAT PAIRS
# --------------------------------

def discover_stat_pairs(header):

    pairs = []

    for i, col in enumerate(header):

        if col.startswith("BaseParam["):
            pairs.append((i, i + 1))

    log(f"Stat pairs detected: {len(pairs)}")

    return pairs


# --------------------------------
# PARSE STATS
# --------------------------------

def parse_stats(row, stat_pairs):

    stats = {}

    for stat_col, val_col in stat_pairs:

        stat_name = normalize(safe_get(row, stat_col))

        val = to_int(safe_get(row, val_col))

        if val <= 0:
            continue

        stats[stat_name] = val

    return stats


# --------------------------------
# LOAD ITEMS
# --------------------------------

def load_all_items():

    rows = load_csv("Item.csv")

    header = rows[1]

    log(f"Item headers detected ({len(header)} columns)")

    name_col = detect_column(header, ["name", "singular"])
    slot_col = detect_column(header, ["equipslot"])
    materia_col = detect_column(header, ["materiaslot"])
    ilvl_col = detect_column(header, ["levelitem", "itemlevel", "level"])

    log(f"Detected columns -> name:{name_col} slot:{slot_col} materia:{materia_col} ilvl:{ilvl_col}")

    stat_pairs = discover_stat_pairs(header)

    items = []
    max_ilvl = 0

    for r in rows[3:]:

        name = safe_get(r, name_col)

        if not name:
            continue

        ilvl = to_int(safe_get(r, ilvl_col))

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


# --------------------------------
# FILTER ITEMS
# --------------------------------

def filter_items(items, min_ilvl):

    filtered = []

    for i in items:

        if to_int(i.get("ilvl")) >= min_ilvl:
            filtered.append(i)

    log(f"Items after ilvl filter ({len(filtered)})")

    return filtered
