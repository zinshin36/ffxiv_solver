from config import STAT_WEIGHTS


def apply_materia(stats, slots, materia_db):

    if slots == 0:
        return stats

    best = None
    best_score = -1

    for materia in materia_db:

        score = 0

        for stat, value in materia["stats"].items():

            weight = STAT_WEIGHTS.get(stat, 0)

            score += value * weight

        if score > best_score:
            best_score = score
            best = materia

    new_stats = stats.copy()

    for stat, value in best["stats"].items():

        new_stats[stat] = new_stats.get(stat, 0) + value * slots

    return new_stats
