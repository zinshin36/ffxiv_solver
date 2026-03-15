def expected_dps(stats):

    main = stats.get("Intelligence", 0)
    crit = stats.get("CriticalHit", 0)
    det = stats.get("Determination", 0)
    dh = stats.get("DirectHitRate", 0)
    sps = stats.get("SpellSpeed", 0)

    crit_rate = 0.05 + crit / 5000
    dh_rate = dh / 5500

    crit_bonus = 1.6

    det_multi = 1 + det / 10000
    speed_multi = 1 + sps / 20000

    return (
        main *
        (1 + crit_rate * (crit_bonus - 1)) *
        (1 + dh_rate * 0.25) *
        det_multi *
        speed_multi
    )
