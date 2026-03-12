from config import STAT_WEIGHTS


def score(stats):

    total = 0

    for s, w in STAT_WEIGHTS.items():

        total += stats.get(s, 0) * w

    return total
