# engine/stats.py

def calc_stats(base_stats, gear_stats, food=None):
    """
    Calculate final stats after gear and food.
    base_stats: dict with base character stats (crit, dh, det, sps, etc.)
    gear_stats: dict with gear contributions
    food: optional dict of stat bonuses
    """
    final_stats = base_stats.copy()

    # Apply gear stats
    for stat, value in gear_stats.items():
        final_stats[stat] = final_stats.get(stat, 0) + value

    # Apply food stats
    if food:
        for stat, value in food.items():
            final_stats[stat] = final_stats.get(stat, 0) + value

    return final_stats

def calc_gcd(det, gcd_base=2.5):
    """
    Calculate GCD based on DET (Determination) stat.
    Formula: GCD = gcd_base * 1000 / (1000 + DET)
    """
    return gcd_base * 1000 / (1000 + det)

def calc_dps(stats, gcd=None, build_type="Crit"):
    """
    Simplified DPS calculation based on stats.
    build_type can prioritize Crit or SPS (Spell Speed)
    """
    crit = stats.get("crit", 0)
    dh = stats.get("dh", 0)
    det = stats.get("det", 0)
    sps = stats.get("sps", 0)

    # Base DPS modifier
    dps = 1.0 + (crit / 1000) + (dh / 1000) + (det / 1000)
    
    # If build_type is SPS, slightly weight GCD
    if build_type.lower() == "spell speed" and gcd:
        dps *= 2.5 / gcd  # faster GCD -> higher effective DPS

    return dps
