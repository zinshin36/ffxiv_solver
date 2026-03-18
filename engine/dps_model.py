def compute_dps(stats):
    crit = stats["crit"]
    dh = stats["dh"]
    det = stats["det"]
    sps = stats["sps"]
    intel = stats.get("int", 1000)

    # simplified scaling but WORKING
    crit_multi = 1 + (crit / 2000)
    dh_multi = 1 + (dh / 2500)
    det_multi = 1 + (det / 3000)
    sps_multi = 1 + (sps / 4000)

    return intel * crit_multi * dh_multi * det_multi * sps_multi
