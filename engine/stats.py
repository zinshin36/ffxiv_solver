from engine.blm_math import gcd_from_sps

# DPS weights
STAT_WEIGHTS_CRIT = {"crit": 1.0, "dh": 0.9, "det": 0.8, "sps": 0.7}
STAT_WEIGHTS_SPS = {"crit": 0.9, "dh": 0.8, "det": 0.7, "sps": 1.0}

def calculate_build_stats(build, food=None, build_type="Crit"):
    stats = {"crit": 0, "dh": 0, "det": 0, "sps": 0, "int": 531}  # default base INT

    # add item stats + melds
    for item in build.values():
        for k, v in item.get("stats", {}).items():
            stats[k] = stats.get(k, 0) + v
        for k, v in item.get("melds", {}).items():
            stats[k] = stats.get(k, 0) + v

    # apply food
    if food:
        for k, v in food.get("stats", {}).items():
            stats[k] = stats.get(k, 0) + v

    # GCD from SPS
    stats["gcd"] = gcd_from_sps(stats.get("sps", 0))

    # DPS calculation based on build type
    weights = STAT_WEIGHTS_CRIT if build_type.lower() == "crit" else STAT_WEIGHTS_SPS
    stats["dps"] = sum(stats.get(k, 0) * w for k, w in weights.items())
    return stats

def cap_stats(stats):
    stats['crit'] = min(stats.get('crit', 0), 3600)
    stats['dh'] = min(stats.get('dh', 0), 3500)
    stats['det'] = min(stats.get('det', 0), 3500)
    stats['sps'] = min(stats.get('sps', 0), 3600)
    return stats
