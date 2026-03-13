# engine/simulator.py
def simulate_dps(gear_set):
    """
    Calculates DPS for a gear set.
    `gear_set` is a dict of item dicts with stats:
    {'Intelligence': int, 'CriticalHit': int, 'Determination': int, 'DirectHit': int, 'SpellSpeed': int, 'WeaponDamage': int}
    """
    total_stats = {}
    for item in gear_set.values():
        for stat, val in item.get("stats", {}).items():
            total_stats[stat] = total_stats.get(stat, 0) + val

    main = total_stats.get("Intelligence", 3000)
    crit = total_stats.get("CriticalHit", 400)
    det = total_stats.get("Determination", 400)
    dh = total_stats.get("DirectHit", 400)
    ss = total_stats.get("SpellSpeed", 400)
    wd = total_stats.get("WeaponDamage", 120)

    crit_mod = 1 + ((crit - 400) / 1900)
    det_mod = 1 + ((det - 400) / 1900)
    dh_mod = 1 + ((dh - 400) / 3300)
    ss_casts = 60 / (2.5 - ((ss - 400) / 1300))

    potency = 320

    return wd * main * crit_mod * det_mod * dh_mod * potency * ss_casts
