def apply_food_stats(base_stats, food_stats):
    """
    Apply food bonuses to base stats.
    base_stats: dict with keys "crit", "dh", "det", "sps"
    food_stats: dict with same keys
    Returns a new dict with combined stats
    """
    result = base_stats.copy()
    for stat, value in food_stats.items():
        if stat in result:
            result[stat] += value
        else:
            result[stat] = value
    return result

def compute_gcd(gcd_base, det):
    """
    Compute actual GCD based on DET stat
    Example formula: gcd = gcd_base * (1000 / (1000 + det))
    """
    return gcd_base * (1000 / (1000 + det))

def compute_dps(stats, gcd, build_type="Crit"):
    """
    Simplified DPS calculation for the purpose of the solver.
    stats: dict containing crit, dh, det, sps
    gcd: float, current gcd
    build_type: string, "Crit" or "Spell Speed"
    Returns DPS float
    """
    crit = stats.get("crit", 0)
    dh = stats.get("dh", 0)
    det = stats.get("det", 0)
    sps = stats.get("sps", 0)

    # Base multipliers (can tweak for balance)
    base_dps = 1000

    # DPS contribution formula (simplified)
    crit_factor = 1 + crit / 1000
    dh_factor = 1 + dh / 1000
    det_factor = 1 + det / 1000
    sps_factor = 1 + sps / 1000

    if build_type.lower() == "crit":
        dps = base_dps * crit_factor * dh_factor * det_factor / gcd
    else:  # Spell Speed focus
        dps = base_dps * sps_factor * dh_factor * det_factor / gcd

    return dps
