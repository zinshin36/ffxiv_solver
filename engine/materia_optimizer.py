import itertools

MATERIA_VALUES = {
    "crit": 36,
    "dh": 36,
    "det": 36,
    "sps": 36
}


def apply_materia(item, max_slots=2):
    """
    Generate all reasonable materia combinations for an item
    """
    stats = item["stats"]

    options = []

    stat_keys = ["crit", "dh", "det", "sps"]

    # generate combinations like (crit, crit), (crit, dh), etc
    for combo in itertools.product(stat_keys, repeat=max_slots):
        new_stats = stats.copy()

        melds = []

        for stat in combo:
            value = MATERIA_VALUES[stat]

            # simple cap: don't exceed +2x base stat (prevents stupidity)
            if new_stats[stat] < stats[stat] * 2:
                new_stats[stat] += value
                melds.append(f"{stat}+{value}")

        options.append({
            "stats": new_stats,
            "melds": melds
        })

    return options


def optimize_materia_for_set(gear_set):
    """
    Try all materia combinations across full gear set
    """
    per_item_options = []

    for item in gear_set:
        per_item_options.append(apply_materia(item))

    best = None
    best_stats = None
    best_melds = None

    # WARNING: this explodes combinatorially (you said that's OK)
    for combo in itertools.product(*per_item_options):

        total_stats = {"crit": 0, "dh": 0, "det": 0, "sps": 0, "int": 0}
        meld_summary = []

        for item, result in zip(gear_set, combo):
            for k in total_stats:
                total_stats[k] += result["stats"].get(k, 0)

            meld_summary.append({
                "item": item["name"],
                "melds": result["melds"]
            })

        if not best:
            best = total_stats
            best_stats = total_stats
            best_melds = meld_summary
            continue

        # simple comparison (real DPS done later)
        if total_stats["crit"] > best["crit"]:
            best = total_stats
            best_stats = total_stats
            best_melds = meld_summary

    return best_stats, best_melds
