from engine.csv_loader import load_csv, to_int
from engine.logger import log


STAT_MAP = {
    "criticalhit": "crit",
    "determination": "det",
    "directhit": "dh",
    "spellspeed": "sps",
    "skill speed": "sks"
}


def normalize(t):
    if not t:
        return ""
    return t.lower().replace("_", "").strip()


def safe_get(row, idx):

    if idx is None or idx >= len(row):
        return ""

    return row[idx]


def detect_column(header, keywords):

    header_norm = [normalize(h) for h in header]

    for i, col in enumerate(header_norm):

        for k in keywords:

            if k in col:
                return i

    return None


# -------------------------------------------------
# LOAD MATERIA
# -------------------------------------------------

def load_materia():

    rows = load_csv("Materia.csv")

    header = rows[1]

    log(f"Materia headers: {header}")

    name_col = detect_column(header, ["name", "singular"])
    stat_col = detect_column(header, ["baseparam"])
    value_col = detect_column(header, ["value"])

    if stat_col is None:
        stat_col = 0

    if value_col is None:
        value_col = 1

    materia = []

    for r in rows[3:]:

        name = safe_get(r, name_col)

        stat_raw = normalize(safe_get(r, stat_col))

        val = to_int(safe_get(r, value_col))

        stat = None

        for k in STAT_MAP:

            if k in stat_raw:
                stat = STAT_MAP[k]

        if stat is None:
            continue

        materia.append({
            "name": name,
            "stat": stat,
            "value": val
        })

    log(f"Materia parsed ({len(materia)})")

    return materia


# -------------------------------------------------
# SIMPLE MATERIA OPTIMIZER
# -------------------------------------------------

def optimize_materia(item, materia_list):

    slots = item.get("materia_slots", 0)

    if slots <= 0:
        return [], item["stats"]

    stats = item["stats"].copy()

    materia_sorted = sorted(materia_list, key=lambda x: x["value"], reverse=True)

    melds = []

    for i in range(slots):

        best = None

        for m in materia_sorted:

            if m["stat"] in ["crit", "det", "dh", "sps"]:
                best = m
                break

        if best:
            melds.append(best)
            stats[best["stat"]] = stats.get(best["stat"], 0) + best["value"]

    return melds, stats
