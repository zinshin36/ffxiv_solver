from itertools import combinations
from engine.simulator import simulate_dps


def get_materia_by_stat(materia):

    stats = {}

    for m in materia:

        stat = m["stat"]
        val = m["value"]

        if stat not in stats or val > stats[stat]:
            stats[stat] = val

    return stats


def apply_materia_layout(item, materia_layout):

    stats = item["stats"].copy()

    for stat, value in materia_layout:

        stats[stat] = stats.get(stat, 0) + value

    return stats


def generate_layouts(item, materia):

    slots = item["MateriaSlots"]

    if slots == 0:
        return [[]]

    best = get_materia_by_stat(materia)

    materia_options = [(k, v) for k, v in best.items()]

    layouts = []

    for combo in combinations(materia_options, min(slots, len(materia_options))):
        layouts.append(combo)

    return layouts


def optimize_item_materia(item, materia):

    layouts = generate_layouts(item, materia)

    best_stats = item["stats"]
    best_score = 0

    for layout in layouts:

        stats = apply_materia_layout(item, layout)

        fake_gear = {"piece": {"stats": stats}}

        score = simulate_dps(fake_gear)

        if score > best_score:
            best_score = score
            best_stats = stats

    return best_stats
