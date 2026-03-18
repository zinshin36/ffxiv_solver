def compute_gcd(spell_speed):
    base = 2.5

    gcd = base * (1000 - (spell_speed - 400) * 130 / 1900) / 1000
    return round(gcd, 3)


# Known BLM tiers (approx)
GCD_TIERS = [
    2.50, 2.48, 2.47, 2.45, 2.44, 2.42,
    2.40, 2.38, 2.37, 2.35, 2.34, 2.32,
    2.30, 2.28, 2.26, 2.24, 2.22, 2.20,
    2.18, 2.16, 2.15
]


def gcd_penalty(gcd, target):
    # snap to nearest tier
    nearest = min(GCD_TIERS, key=lambda x: abs(x - gcd))

    # strong penalty if missing tier
    return abs(nearest - target) * 1500
