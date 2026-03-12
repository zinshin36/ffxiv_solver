from config import STAT_WEIGHTS


def score(stats):

    total = 0

    for stat, weight in STAT_WEIGHTS.items():

        value = stats.get(stat, 0)

        total += value * weight

    return total
