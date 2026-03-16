def compute_dps(stats):

    int_stat = stats.get("int", 0)
    crit = stats.get("crit", 0)
    det = stats.get("det", 0)
    dh = stats.get("dh", 0)
    sps = stats.get("sps", 0)

    dps = (
        int_stat * 1.0 +
        crit * 0.45 +
        det * 0.30 +
        dh * 0.35 +
        sps * 0.18
    )

    return dps
