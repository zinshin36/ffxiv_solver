from itertools import combinations_with_replacement
from engine.csv_loader import load_csv, to_int

MAX_OVERMELD = 5


def load_materia():

    materia_rows = load_csv("Materia.csv")
    param_rows = load_csv("MateriaParam.csv")

    param_map = {}

    for r in param_rows[1:]:

        materia_id = r[1]
        stat = r[2]
        value = to_int(r[3])

        param_map[materia_id] = (stat, value)

    materia = []

    for r in materia_rows[1:]:

        key = r[0]
        name = r[1]

        if key not in param_map:
            continue

        stat, value = param_map[key]

        materia.append({
            "name": name,
            "stat": stat,
            "value": value
        })

    return materia


def apply_melds(base_stats, melds):

    stats = base_stats.copy()

    for m in melds:
        stats[m["stat"]] = stats.get(m["stat"], 0) + m["value"]

    return stats


def generate_meld_sets(item, materia):

    slot_count = max(item["materia_slots"], MAX_OVERMELD)

    # limit materia search to strongest ones
    materia_sorted = sorted(
        materia,
        key=lambda x: x["value"],
        reverse=True
    )[:6]

    meld_sets = []

    for meld_combo in combinations_with_replacement(materia_sorted, slot_count):

        meld_sets.append(list(meld_combo))

    return meld_sets


def optimize_item_melds(item, materia, stat_eval):

    best_stats = None
    best_melds = []
    best_score = -1

    meld_sets = generate_meld_sets(item, materia)

    for melds in meld_sets:

        stats = apply_melds(item["stats"], melds)

        score = stat_eval(stats)

        if score > best_score:
            best_score = score
            best_stats = stats
            best_melds = melds

    return best_stats, best_melds
