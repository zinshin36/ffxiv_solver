from engine.csv_loader import load_csv, to_int
from engine.logger import log


NAME_COL = 1
ILVL_COL = 12
SLOT_COL = 18
MATERIA_COL = 87


def safe_get(row, idx):
    if idx >= len(row):
        return ""
    return row[idx]


def discover_stat_pairs(header):

    pairs = []

    for i, col in enumerate(header):
        if "BaseParam" in col:
            pairs.append((i, i + 1))

    log(f"Stat pairs detected: {len(pairs)}")

    return pairs


def parse_stats(row, stat_pairs):

    stats = {}

    for stat_col, val_col in stat_pairs:

        stat_name = safe_get(row, stat_col)
        val = to_int(safe_get(row, val_col))

        if val <= 0:
            continue

        stats[stat_name] = val

    return stats


def load_all_items():

    rows = load_csv("Item.csv")

    header = rows[1]

    log(f"Item headers detected ({len(header)} columns)")

    stat_pairs = discover_stat_pairs(header)

    items = []
    max_ilvl = 0

    sample = []

    for r in rows[3:]:

        name = safe_get(r, NAME_COL)

        if not name:
            continue

        ilvl = to_int(safe_get(r, ILVL_COL))
        slot = safe_get(r, SLOT_COL)
        materia_slots = to_int(safe_get(r, MATERIA_COL))

        stats = parse_stats(r, stat_pairs)

        if len(sample) < 10:
            sample.append(ilvl)

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

    log(f"Sample detected ilvls: {sample}")
    log(f"Items parsed ({len(items)})")
    log(f"Highest item level detected: {max_ilvl}")

    return items, max_ilvl


def filter_items(items, min_ilvl):

    filtered = []

    for i in items:
        if i["ilvl"] >= min_ilvl:
            filtered.append(i)

    log(f"Items after ilvl filter ({len(filtered)})")

    return filtered
