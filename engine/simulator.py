def score(gear_set):
    """Compute a DPS score using stats including materia."""
    total = {}

    for item in gear_set.values():
        for stat, val in item.get("stats", {}).items():
            total[stat] = total.get(stat, 0) + val

    main = total.get("Intelligence", 3000)
    crit = total.get("CriticalHit", 400)
    det = total.get("Determination", 400)
    dh = total.get("DirectHit", 400)
    ss = total.get("SpellSpeed", 400)
    wd = total.get("WeaponDamage", 120)

    crit_mod = 1 + ((crit - 400) / 1900)
    det_mod = 1 + ((det - 400) / 1900)
    dh_mod = 1 + ((dh - 400) / 3300)
    ss_casts = 60 / (2.5 - ((ss - 400) / 1300))

    potency = 320

    return wd * main * crit_mod * det_mod * dh_mod * potency * ss_casts
