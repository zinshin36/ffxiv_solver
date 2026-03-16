from engine.csv_loader import load_csv, to_int
from engine.logger import log


STAT_MAP = {
    "criticalhit": "crit",
    "determination": "det",
    "directhit": "dh",
    "spellspeed": "sps",
    "intelligence": "int"
}


def normalize(t):
    return t.lower().replace(" ", "").replace("_", "")


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
# LOAD MATERIA
# -------------------------

def load_materia():

    rows = load_csv("Materia.csv")

    header = rows[1]

    name_col = detect_column(header, ["name", "singular"])
    stat_col = detect_column(header, ["baseparam"])
    value_col = detect_column(header, ["value"])

    materia = []

    for r in rows[3:]:

        name = safe_get(r, name_col)

        if not name:
            continue

        stat_raw = normalize(safe_get(r, stat_col))

        stat = None

        for k in STAT_MAP:

            if k in stat_raw:
                stat = STAT_MAP[k]

        if not stat:
            continue

        value = to_int(safe_get(r, value_col))

        materia.append({
            "name": name,
            "stat": stat,
            "value": value
        })

    log(f"Materia parsed ({len(materia)})")

    return materia


# -------------------------
# MATERIA OPTIMIZATION
# -------------------------

def optimize_materia(item, materia_list):

    slots = item.get("materia_slots", 0)

    if slots == 0:
        return [], {}

    stats = item["stats"].copy()

    melds = []

    # sort materia by value (largest first)
    materia_sorted = sorted(materia_list, key=lambda x: x["value"], reverse=True)

    for i in range(slots):

        best = None

        for m in materia_sorted:

            stat = m["stat"]

            # prioritize BLM stats
            if stat not in ["crit", "det", "dh", "sps"]:
                continue

            best = m
            break

        if best:

            melds.append(best)

            stats[best["stat"]] = stats.get(best["stat"], 0) + best["value"]

    return melds, stats
