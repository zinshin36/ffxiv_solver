def calculate_gcd(sps):
    """
    Approximate FFXIV GCD formula for casters
    """
    base = 2.5

    # simplified but good enough
    gcd = base - (sps / 10000)

    return max(2.0, min(2.5, gcd))


def calculate_score(stats, target_gcd):

    if not stats:
        return 0

    crit = stats.get("crit", 0)
    dh = stats.get("dh", 0)
    det = stats.get("det", 0)
    sps = stats.get("sps", 0)

    # --- GCD ---
    gcd = calculate_gcd(sps)

    # ❗ SOFT MATCH instead of hard fail
    gcd_diff = abs(gcd - target_gcd)

    # penalty instead of rejection
    gcd_penalty = max(0.7, 1 - (gcd_diff * 2))

    # --- STAT WEIGHTS (BLM-friendly) ---
    score = (
        crit * 1.0 +
        dh * 0.9 +
        det * 0.8 +
        sps * 0.7
    )

    return score * gcd_penalty
