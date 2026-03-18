def compute_dps(stats):
    crit = stats["crit"]
    dh = stats["dh"]
    det = stats["det"]
    sps = stats["sps"]
    intel = stats.get("int", 1000)

    # scaling
    crit_multi = 1 + (crit / 1900)
    dh_multi = 1 + (dh / 2300)
    det_multi = 1 + (det / 2700)

    # SPELL SPEED BREAKPOINT VALUE
    if sps >= 1400:
        sps_multi = 1.12
    elif sps >= 1200:
        sps_multi = 1.09
    elif sps >= 1000:
        sps_multi = 1.06
    else:
        sps_multi = 1.02

    return intel * crit_multi * dh_multi * det_multi * sps_multi
