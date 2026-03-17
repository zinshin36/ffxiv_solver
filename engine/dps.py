def calculate_score(stats, target_gcd):

    crit = stats.get("crit", 0)
    dh = stats.get("dh", 0)
    det = stats.get("det", 0)
    sps = stats.get("sps", 0)

    score = (
        crit * 1.0
        + dh * 0.9
        + det * 0.7
        + sps * 0.6
    )

    if target_gcd == "2.46":
        score += sps * 0.2

    if target_gcd == "2.44":
        score += sps * 0.3

    return score
