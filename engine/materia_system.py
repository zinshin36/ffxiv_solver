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

    slots = max(item["materia_slots"], MAX_OVERMELD)

    materia = sorted(materia, key=lambda x: x["value"], reverse=True)[:6]

    return combinations_with_replacement(materia, slots)


def optimize_item_melds(item, materia, score_func):

    best_stats = None
    best_melds = []
    best_score = -1

    for melds in generate_meld_sets(item, materia):

        stats = apply_melds(item["stats"], melds)

        score = score_func(stats)

        if score > best_score:
            best_score = score
            best_stats = stats
            best_melds = melds

    return best_stats, best_melds
