import math

BASE_GCD = 2.5
LEVEL_MOD = 1900
BASE_STAT = 400


def gcd_from_sps(sps):

    if sps <= BASE_STAT:
        return BASE_GCD

    gcd = math.floor(
        BASE_GCD *
        (1000 - math.floor(130 * (sps - BASE_STAT) / LEVEL_MOD))
        / 1000
    )

    return round(gcd, 3)


def find_sps_tiers(min_sps=400, max_sps=3000):

    tiers = {}

    for sps in range(min_sps, max_sps):

        gcd = gcd_from_sps(sps)

        if gcd not in tiers:
            tiers[gcd] = sps

    return tiers


def tier_bonus(sps, target_gcd):

    gcd = gcd_from_sps(sps)

    diff = abs(gcd - target_gcd)

    if diff < 0.005:
        return 1000

    if diff < 0.02:
        return 200

    return 0
