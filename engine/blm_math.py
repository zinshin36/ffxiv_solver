import math

BASE_GCD = 2.5
LEVEL_MOD = 1900
BASE_STAT = 400


def gcd_from_sps(spell_speed):

    if spell_speed <= 0:
        return BASE_GCD

    gcd = math.floor(
        BASE_GCD * (1000 - math.floor(130 * (spell_speed - BASE_STAT) / LEVEL_MOD)) / 1000
    )

    return round(gcd, 3)


def gcd_score(spell_speed, target):

    gcd = gcd_from_sps(spell_speed)

    bonus = (2.5 - gcd) * 120

    if target:
        diff = abs(gcd - target)

        if diff < 0.01:
            bonus += 800
        elif diff < 0.02:
            bonus += 200

    return bonus
