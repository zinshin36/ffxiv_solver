import math


def crit_multiplier(crit):

    rate = (crit - 400) / 1900 + 0.05
    dmg = (crit - 400) / 1900 + 1.4

    return 1 + rate * (dmg - 1)


def dh_multiplier(dh):

    rate = (dh - 400) / 1900

    return 1 + rate * 0.25


def det_multiplier(det):

    return 1 + (det - 390) / 1900


def sps_multiplier(sps):

    return 1 + (sps - 400) / 2000


def compute_dps(stats):

    INT = stats.get("int", 0)

    crit = stats.get("crit", 0)
    dh = stats.get("dh", 0)
    det = stats.get("det", 0)
    sps = stats.get("sps", 0)

    base = INT

    dmg = (
        base *
        crit_multiplier(crit) *
        dh_multiplier(dh) *
        det_multiplier(det) *
        sps_multiplier(sps)
    )

    return dmg
