from itertools import product

from engine.dps_model import compute_dps
from engine.materia_system import best_materia
from engine.food_system import apply_food


def group_slots(items):

    slots = {}

    for i in items:

        slot = i["slot"]

        if slot not in slots:
            slots[slot] = []

        slots[slot].append(i)

    return slots


def combine_stats(items):

    stats = {}

    for g in items:

        for k, v in g["stats"].items():

            stats[k] = stats.get(k, 0) + v

    return stats


def ring_rule(combo):

    rings = [i for i in combo if "Ring" in i["name"]]

    if len(rings) < 2:
        return True

    return rings[0]["name"] != rings[1]["name"]


def solve(items, materia, food):

    slots = group_slots(items)

    slot_lists = list(slots.values())

    best = []

    for combo in product(*slot_lists):

        if not ring_rule(combo):
            continue

        melded_items = []
        melds = []

        for g in combo:

            s, m = best_materia(g, materia)

            melded_items.append(s)
            melds.append((g["name"], m))

        stats = {}

        for s in melded_items:

            for k, v in s.items():
                stats[k] = stats.get(k, 0) + v

        stats = apply_food(stats, food)

        dps = compute_dps(stats)

        best.append((dps, melds, stats))

        best = sorted(best, reverse=True)[:5]

    return best
