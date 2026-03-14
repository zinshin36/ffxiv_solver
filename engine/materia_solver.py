from itertools import combinations
from engine.simulator import simulate_dps


def get_best_materia(materia):

    stats = {}

    for m in materia:

        stat = m["stat"]
        value = m["value"]

        if stat not in stats or value > stats[stat]:
            stats[stat] = value

    return stats


def apply_layout(base_stats, layout):

    stats = base_stats.copy()

    for stat, val in layout:
        stats[stat] = stats.get(stat, 0) + val

    return stats


def generate_layouts(slots, materia):

    if slots <= 0:
        return [[]]

    best = get_best_materia(materia)

    options = [(k, v) for k, v in best.items()]

    layouts = []

    for combo in combinations(options, min(slots, len(options))):
        layouts.append(combo)

    return layouts


def optimize_item_materia(item, materia):

    slots = item["MateriaSlots"]

    layouts = generate_layouts(slots, materia)

    best_stats = item["stats"]
    best_score = 0

    for layout in layouts:

        stats = apply_layout(item["stats"], layout)

        fake = {"piece": {"stats": stats}}

        score = simulate_dps(fake)

        if score > best_score:
            best_score = score
            best_stats = stats

    return best_stats
