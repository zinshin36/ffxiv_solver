import math


# =========================
# FFXIV GCD FORMULA (APPROX)
# =========================
def calculate_gcd(spell_speed):
    """
    Realistic approximation of FFXIV GCD formula
    """
    base_gcd = 2.5

    gcd = base_gcd * (1000 - math.floor(130 * (spell_speed - 400) / 1900)) / 1000

    return round(gcd, 3)


# =========================
# SPEED TIERS
# =========================
def get_speed_tier(spell_speed):
    gcd = calculate_gcd(spell_speed)

    # Known BLM tiers (approx)
    tiers = [
        2.50, 2.48, 2.46, 2.44, 2.42,
        2.40, 2.38, 2.36, 2.34, 2.32,
        2.30, 2.28, 2.26, 2.24, 2.22, 2.20
    ]

    closest = min(tiers, key=lambda t: abs(t - gcd))

    return closest


# =========================
# FILTER BY TARGET TIER
# =========================
def meets_speed_target(spell_speed, target_gcd):
    actual = calculate_gcd(spell_speed)

    return actual <= target_gcd
