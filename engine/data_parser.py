from engine.csv_loader import load_csv, to_int
from engine.logger import log


STAT_NAMES = {
    "critical hit": "crit",
    "determination": "det",
    "direct hit": "dh",
    "spell speed": "sps",
    "intelligence": "int"
}


def normalize(text):
    return text.lower().replace(" ", "").replace("_", "")


def discover_columns(header):

    cols = {}

    normalized = [normalize(h) for h in header]

    for i, h in enumerate(normalized):

        if "name" == h:
            cols["name"] = i

        elif "equipslotcategory" in h:
            cols["slot"] = i

        elif "materiaslotcount" in h:
            cols["materia_slots"] = i

        elif "level" in h and "item" in h:
            cols["ilvl"] = i

        elif "levelitem" == h:
            cols["ilvl"] = i

        elif h == "level":
            cols["ilvl"] = i

    missing = []

    for k in ["name", "slot", "materia_slots", "ilvl"]:
        if k not in cols:
            missing.append(k)

    if missing:
        raise Exception(f"Required columns missing: {missing}")

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

        if stat_col >= len(row):
            continue

        stat_name = row[stat_col]

        if not stat_name:
            continue

        key = normalize(stat_name)

        for name in STAT_NAMES:

            if name.replace(" ", "") in key:
                stats[STAT_NAMES[name]] = to_int(row[val_col])

    return stats


def load_all_items():

    rows = load_csv("Item.csv")

    header = rows[1]

    columns = discover_columns(header)

    stat_pairs = discover_stat_pairs(header)

    items = []
    max_ilvl = 0

    for r in rows[3:]:

        if len(r) <= columns["name"]:
            continue

        name = r[columns["name"]]

        if not name:
            continue

        ilvl = to_int(r[columns["ilvl"]])

        slot = r[columns["slot"]]

        materia_slots = to_int(r[columns["materia_slots"]])

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
