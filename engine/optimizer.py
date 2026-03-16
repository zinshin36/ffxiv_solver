from engine.logger import log
from engine.data_parser import filter_items
from engine.materia_system import optimize_materia


def score_build(stats):

    crit = stats.get("criticalhit", 0)
    det = stats.get("determination", 0)
    dh = stats.get("directhitrate", 0)
    sps = stats.get("spellspeed", 0)

    return crit * 1.0 + det * 0.9 + dh * 0.95 + sps * 0.85


def solve(items, materia, min_ilvl):

    items = filter_items(items, min_ilvl)

    if not items:
        log("No items after filter")
        return []

    best_builds = []

    for item in items:

        melds, stats = optimize_materia(item, materia)

        score = score_build(stats)

        build = {
            "item": item["name"],
            "ilvl": item["ilvl"],
            "score": score,
            "melds": melds
        }

        best_builds.append(build)

    best_builds.sort(key=lambda x: x["score"], reverse=True)

    log(f"Solver finished ({len(best_builds)} builds evaluated)")

    return best_builds[:5]
