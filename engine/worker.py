from engine.materia_solver import best_materia
from engine.simulator import score


def evaluate(combo, materia):

    total = {}

    for item in combo:

        stats = best_materia(item["stats"], item["materia_slots"], materia)

        for k, v in stats.items():
            total[k] = total.get(k, 0) + v

    dps = score(total)

    return (combo, dps)
