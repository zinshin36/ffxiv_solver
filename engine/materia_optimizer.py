import itertools

MATERIA_VALUES = {
    "crit": 36,
    "dh": 36,
    "det": 36,
    "sps": 36
}

STAT_KEYS = ["crit", "dh", "det", "sps"]


def get_max_slots(item):
    base = item.get("materia_slots", 0)

    # overmeld support
    if item.get("is_overmeldable", True):
        return base + 2

    return base


def apply_materia(item):
    slots = get_max_slots(item)

    base_stats = item["stats"]

    options = []

    for combo in itertools.product(STAT_KEYS, repeat=slots):

        stats = base_stats.copy()
        melds = []

        for stat in combo:
            stats[stat] += MATERIA_VALUES[stat]
            melds.append(f"{stat}+{MATERIA_VALUES[stat]}")

        options.append({
            "stats": stats,
            "melds": melds
        })

    return options


def optimize_materia_for_set(gear_set):

    per_item = [apply_materia(i) for i in gear_set]

    best = None
    best_stats = None
    best_melds = None

    for combo in itertools.product(*per_item):

        total = {"crit": 0, "dh": 0, "det": 0, "sps": 0, "int": 0}
        melds = []

        for item, result in zip(gear_set, combo):

            for k in total:
                total[k] += result["stats"].get(k, 0)

            melds.append({
                "item": item["name"],
                "melds": result["melds"]
            })

        if not best or total["crit"] > best["crit"]:
            best = total
            best_stats = total
            best_melds = melds

    return best_stats, best_melds
