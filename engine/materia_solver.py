from itertools import product

MATERIA_VALUES = {
    "crit": 36,
    "dh": 36,
    "det": 36,
    "sps": 36
}

MATERIA_TYPES = ["crit", "dh", "det", "sps"]


def generate_melds(slots):
    return list(product(MATERIA_TYPES, repeat=slots))


def apply_melds(base_stats, melds):
    stats = base_stats.copy()

    for m in melds:
        stats[m] += MATERIA_VALUES[m]

    return stats


def optimize_materia(base_stats, slots, compute_dps, gcd_func, target_gcd):
    best = None

    meld_sets = generate_melds(slots)

    for melds in meld_sets:
        stats = apply_melds(base_stats, melds)

        gcd = gcd_func(stats["sps"])
        dps = compute_dps(stats)

        # GCD penalty (VERY IMPORTANT)
        penalty = abs(gcd - target_gcd) * 1000
        final_score = dps - penalty

        if not best or final_score > best["score"]:
            best = {
                "stats": stats,
                "score": final_score,
                "melds": melds,
                "gcd": gcd,
                "dps": dps
            }

    return best
