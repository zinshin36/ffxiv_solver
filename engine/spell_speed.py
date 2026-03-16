def gcd_from_sps(sps):

    base = 2.5

    gcd = base * (1000 - (130 * (sps - 400) / 1900)) / 1000

    return round(gcd, 3)


def matches_target(sps, target):

    return abs(gcd_from_sps(sps) - target) <= 0.01
