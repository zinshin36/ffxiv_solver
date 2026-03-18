def compute_gcd(spell_speed):
    base = 2.5

    # simplified but effective FFXIV formula
    gcd = base * (1000 - (spell_speed - 400) * 130 / 1900) / 1000

    return round(gcd, 3)
