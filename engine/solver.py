from itertools import product
from engine.materia_solver import apply_materia
from engine.simulator import score
from config import MAX_RESULTS


def combine_stats(items):

    stats = {}

    for item in items:

        for k, v in item.items():
            stats[k] = stats.get(k, 0) + v

    return stats


def solve(slot_map, materia_db):

    slot_lists = list(slot_map.values())

    results = []

    for combo in product(*slot_lists):

        stat_list = []

        for item in combo:

            stats = apply_materia(item["stats"], item["materia_slots"], materia_db)

            stat_list.append(stats)

        combined = combine_stats(stat_list)

        dps = score(combined)

        results.append({
            "gear": combo,
            "dps": dps
        })

    results.sort(key=lambda x: x["dps"], reverse=True)

    return results[:MAX_RESULTS]
