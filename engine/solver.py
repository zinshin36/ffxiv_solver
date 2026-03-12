from itertools import product
from multiprocessing import Pool

from config import MAX_RESULTS, CPU_WORKERS
from engine.worker import evaluate


def solve(slots, materia):

    combos = list(product(*slots.values()))

    with Pool(CPU_WORKERS) as p:

        results = p.starmap(evaluate, [(c, materia) for c in combos])

    results.sort(key=lambda x: x[1], reverse=True)

    return results[:MAX_RESULTS]
