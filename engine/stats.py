from engine.dps_model import compute_dps, gcd_from_sps

BASE_STATS = {
    'hp': 4862,
    'int': 531,
    'crit': 420,
    'dh': 420,
    'det': 440,
    'sps': 420
}

def calculate_build_stats(build, food=None, foods=None):

    stats = BASE_STATS.copy()

    # Add gear stats
    for item in build.values():
        for k, v in item["stats"].items():
            stats[k] += v

        # Apply melds
        for stat, value in item.get("melds", {}).items():
            stats[stat] += value

    # Apply food
    if food and foods:
        for f in foods:
            if f["name"] == food:
                for k, v in f["stats"].items():
                    stats[k] += v

    # Compute GCD + DPS
    stats["gcd"] = gcd_from_sps(stats["sps"])
    stats["dps"] = compute_dps(stats)

    return stats


def cap_stats(stats):
    # prevent absurd overflow
    stats["crit"] = min(stats["crit"], 4000)
    stats["dh"] = min(stats["dh"], 4000)
    stats["det"] = min(stats["det"], 4000)
    stats["sps"] = min(stats["sps"], 4000)
    return stats
