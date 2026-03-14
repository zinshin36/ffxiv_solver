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


def gcd_bonus(spell_speed, target_gcd=None):

    gcd = gcd_from_sps(spell_speed)

    # reward faster tiers
    bonus = (2.5 - gcd) * 120

    # if a target gcd is provided prioritize hitting it
    if target_gcd:

        diff = abs(gcd - target_gcd)

        # strong reward for matching tier
        bonus += max(0, (0.02 - diff)) * 2000

    return bonus
