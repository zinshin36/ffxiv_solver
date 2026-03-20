import math

# ----------------------------------------
# LEVEL CONSTANTS (Lv100 approximation)
# ----------------------------------------
LEVEL_SUB = 400
LEVEL_DIV = 1900
LEVEL_MAIN = 390

# ----------------------------------------
# CRIT
# ----------------------------------------
def crit_rate(crit):
    return math.floor(200 * (crit - LEVEL_SUB) / LEVEL_DIV + 50) / 1000

def crit_damage(crit):
    return (1400 + math.floor(200 * (crit - LEVEL_SUB) / LEVEL_DIV)) / 1000

# ----------------------------------------
# DIRECT HIT
# ----------------------------------------
def dh_rate(dh):
    return math.floor(550 * (dh - LEVEL_SUB) / LEVEL_DIV) / 1000

# ----------------------------------------
# DETERMINATION
# ----------------------------------------
def det_multiplier(det):
    return (1000 + math.floor(140 * (det - LEVEL_MAIN) / LEVEL_DIV)) / 1000

# ----------------------------------------
# SPELL SPEED
# ----------------------------------------
def speed_multiplier(sps):
    return (1000 + math.floor(130 * (sps - LEVEL_SUB) / LEVEL_DIV)) / 1000

# ----------------------------------------
# GCD
# ----------------------------------------
def gcd_from_sps(sps):
    base = 2.5
    gcd = base * (1000 - math.floor(130 * (sps - LEVEL_SUB) / LEVEL_DIV)) / 1000
    return round(gcd, 3)

# ----------------------------------------
# FINAL DPS MODEL
# ----------------------------------------
def compute_dps(stats):

    crit = stats.get("crit", 0)
    dh = stats.get("dh", 0)
    det = stats.get("det", 0)
    sps = stats.get("sps", 0)
    intel = stats.get("int", 1000)

    cr = crit_rate(crit)
    cd = crit_damage(crit)
    dr = dh_rate(dh)
    dm = det_multiplier(det)
    sm = speed_multiplier(sps)

    # Expected value model
    crit_expected = 1 + cr * (cd - 1)
    dh_expected = 1 + dr * 0.25

    return intel * crit_expected * dh_expected * dm * sm
