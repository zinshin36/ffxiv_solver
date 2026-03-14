def simulate_dps(gear_set):

    total = {}

    for piece in gear_set.values():

        for stat, val in piece["stats"].items():

            total[stat] = total.get(stat, 0) + int(val)

    main = total.get("Intelligence", 3000)
    crit = total.get("CriticalHit", 400)
    det = total.get("Determination", 400)
    dh = total.get("DirectHit", 400)
    ss = total.get("SpellSpeed", 400)
    wd = total.get("WeaponDamage", 120)

    crit_mod = 1 + ((crit - 400) / 1900)
    det_mod = 1 + ((det - 400) / 1900)
    dh_mod = 1 + ((dh - 400) / 3300)

    casts = 60 / (2.5 - ((ss - 400) / 1300))

    potency = 320

    dps = wd * main * crit_mod * det_mod * dh_mod * potency * casts

    return dps
