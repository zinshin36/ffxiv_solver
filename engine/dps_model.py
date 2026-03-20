import math

# -------------------------
# LEVEL CONSTANTS (Lv90 approx)
# -------------------------
LEVEL_MAIN = 390
LEVEL_SUB = 400
LEVEL_DIV = 1900


# -------------------------
# CRIT
# -------------------------
def crit_rate(crit):
    return math.floor(200 * (crit - LEVEL_SUB) / LEVEL_DIV + 50) / 1000


def crit_damage(crit):
    return (1400 + math.floor(200 * (crit - LEVEL_SUB) / LEVEL_DIV)) / 1000


# -------------------------
# DIRECT HIT
# -------------------------
def dh_rate(dh):
    return math.floor(550 * (dh - LEVEL_SUB) / LEVEL_DIV) / 1000


# -------------------------
# DETERMINATION
# -------------------------
def det_multiplier(det):
    return (1000 + math.floor(140 * (det - LEVEL_MAIN) / LEVEL_DIV)) / 1000


# -------------------------
# SPELL SPEED
# -------------------------
def speed_multiplier(sps):
    return (1000 + math.floor(130 * (sps - LEVEL_SUB) / LEVEL_DIV)) / 1000


def compute_gcd_from_sps(sps):
    base = 2500  # ms

    speed_mod = math.ceil(130 * (LEVEL_SUB - sps) / LEVEL_DIV)

    gcd = math.floor((base * (1000 + speed_mod)) / 10000) / 100

    return round(gcd, 3)


# -------------------------
# FINAL DPS MODEL
# -------------------------
def compute_dps(stats):

    crit = stats["crit"]
    dh = stats["dh"]
    det = stats["det"]
    sps = stats["sps"]
    intel = stats.get("int", 1000)

    # --- components ---
    c_rate = crit_rate(crit)
    c_dmg = crit_damage(crit)

    dh_chance = dh_rate(dh)

    det_mult = det_multiplier(det)
    spd_mult = speed_multiplier(sps)

    # --- expected multipliers ---
    crit_expected = 1 + (c_rate * (c_dmg - 1))
    dh_expected = 1 + (dh_chance * 0.25)

    # --- final ---
    damage = intel * det_mult * spd_mult * crit_expected * dh_expected

    return damage
