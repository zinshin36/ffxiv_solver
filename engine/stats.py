from engine.dps_model import compute_dps, gcd_from_sps
from engine.food_system import apply_food

def calculate_build_stats(build, selected_food=None):
    stats = {"crit":0, "dh":0, "det":0, "sps":0, "int":531}  # base int for BLM

    # Apply items and melds
    for item in build.values():
        for k,v in item.get("stats", {}).items():
            stats[k] = stats.get(k, 0) + v
        for k,v in item.get("melds", {}).items():
            stats[k] = stats.get(k, 0) + v

    # Apply food
    if selected_food:
        stats = apply_food(stats, selected_food)

    # Calculate GCD
    stats['gcd'] = gcd_from_sps(stats.get("sps", 0))

    # Compute DPS
    stats['dps'] = compute_dps(stats)

    return stats

def cap_stats(stats):
    stats['crit'] = min(stats['crit'], 3600)
    stats['dh'] = min(stats['dh'], 3500)
    stats['det'] = min(stats['det'], 3500)
    stats['sps'] = min(stats['sps'], 3600)
    return stats
