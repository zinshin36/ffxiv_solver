def calculate_build_stats(build, food=None):
    # Base example stats from your last message
    base = {'hp':4862,'int':531,'crit':420,'dh':420,'det':440,'sps':420}
    stats = base.copy()

    # Apply item stats + melds
    for item in build.values():
        for k,v in item.get('stats', {}).items():
            stats[k] += v
        for k,v in item.get('melds', {}).items():
            stats[k] += v

    # Apply food
    if food:
        for k,v in food.get('stats', {}).items():
            stats[k] += v

    # GCD calc
    stats['gcd'] = 2.5  # placeholder, calculate from sps if needed

    # DPS formula placeholder
    stats['dps'] = stats['crit']*10 + stats['dh']*5 + stats['sps']*3
    return stats

def cap_stats(stats):
    # Cap stats based on FFXIV limits
    stats['crit'] = min(stats['crit'], 3600)
    stats['dh'] = min(stats['dh'], 3500)
    stats['det'] = min(stats['det'], 3500)
    stats['sps'] = min(stats['sps'], 3600)
    return stats
