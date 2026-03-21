def apply_food(stats, food):
    """
    Apply a food buff to the given stats dictionary.
    'food' must be a dict with a 'stats' key containing stat bonuses.
    """
    if not food or "stats" not in food:
        return stats

    new_stats = stats.copy()
    for stat, value in food["stats"].items():
        new_stats[stat] = new_stats.get(stat, 0) + value
    return new_stats
