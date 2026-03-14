import math

BASE_GCD = 2.5
LEVEL_MOD = 1900
BASE_STAT = 400


def gcd_from_sps(sps):

    if sps <= 0:
        return BASE_GCD

    gcd = math.floor(
        BASE_GCD *
        (1000 - math.floor(130 * (sps - BASE_STAT) / LEVEL_MOD))
        / 1000
    )

    return round(gcd, 3)


def gcd_bonus(sps, target):

    gcd = gcd_from_sps(sps)

    score = (2.5 - gcd) * 150

    if target:

        diff = abs(gcd - target)

        if diff < 0.01:
            score += 800

        elif diff < 0.02:
            score += 200

    return score
