from config import STAT_WEIGHTS


def best_materia(stats, slots, materia_db):

    if slots == 0:
        return stats

    best = None
    best_score = -1

    for m in materia_db:

        score = 0

        for s, v in m["stats"].items():

            weight = STAT_WEIGHTS.get(s, 0)

            score += v * weight

        if score > best_score:

            best_score = score
            best = m

    out = stats.copy()

    for s, v in best["stats"].items():

        out[s] = out.get(s, 0) + v * slots

    return out
