from engine.csv_loader import load_csv, to_int
from engine.logger import log


STAT_NAMES = {
    "criticalhit": "crit",
    "determination": "det",
    "directhit": "dh",
    "spellspeed": "sps",
    "intelligence": "int"
}


def normalize(text):

    return text.lower().replace(" ", "").replace("_", "")


def safe_get(row, index):

    if index >= len(row):
        return ""

    return row[index]


def discover_columns(header):

    cols = {}

    for i, h in enumerate(header):

        n = normalize(h)

        if n == "name":
            cols["name"] = i

        elif "equipslotcategory" in n:
            cols["slot"] = i

        elif "materiaslotcount" in n:
            cols["materia"] = i

        elif "level" in n and "item" in n:
            cols["ilvl"] = i

        elif n == "level":
            cols["ilvl"] = i

    required = ["name", "slot", "materia", "ilvl"]

    missing = [x for x in required if x not in cols]

    if missing:
        raise Exception(f"Missing required columns: {missing}")

    log(f"Detected columns: {cols}")

    return cols


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

        stat_name = normalize(safe_get(row, stat_col))

        if not stat_name:
            continue

        for key in STAT_NAMES:

            if key in stat_name:

                stats[STAT_NAMES[key]] = to_int(safe_get(row, val_col))

    return stats


def load_all_items():

    rows = load_csv("Item.csv")

    header = rows[1]

    cols = discover_columns(header)

    stat_pairs = discover_stat_pairs(header)

    items = []
    max_ilvl = 0

    for r in rows[3:]:

        name = safe_get(r, cols["name"])

        if not name:
            continue

        ilvl = to_int(safe_get(r, cols["ilvl"]))

        slot = safe_get(r, cols["slot"])

        materia_slots = to_int(safe_get(r, cols["materia"]))

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
