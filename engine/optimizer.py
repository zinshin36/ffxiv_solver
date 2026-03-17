from engine.logger import log
from engine.gear_pruner import prune_slot
from engine.dps import calculate_score


def group_by_slot(items):

    slots = {}

    for item in items:

        slot = item["slot"]

        if slot not in slots:
            slots[slot] = []

        slots[slot].append(item)

    return slots


def solve(items, target_gcd, progress_callback=None):

    log("Starting solver")

    slots = group_by_slot(items)

    for slot in slots:
        slots[slot] = prune_slot(slots[slot])

    slot_list = list(slots.values())

    best = []
    checked = 0

    def dfs(slot_index, build, stats):

        nonlocal checked

        if slot_index >= len(slot_list):

            checked += 1

            if checked % 2000 == 0:

                log(f"Checked {checked} builds")

                if progress_callback:
                    progress_callback(checked)

            score = calculate_score(stats, target_gcd)

            best.append((score, build.copy()))

            best.sort(reverse=True)

            if len(best) > 10:
                best.pop()

            return

        for item in slot_list[slot_index]:

            new_stats = stats.copy()

            for stat in ["crit", "dh", "det", "sps"]:
                new_stats[stat] = new_stats.get(stat, 0) + item.get(stat, 0)

            build.append(item)

            dfs(slot_index + 1, build, new_stats)

            build.pop()

    dfs(0, [], {})

    log("Solver finished")

    results = []

    rank = 1

    for score, build in best:

        results.append({
            "rank": rank,
            "score": round(score, 2),
            "items": [i["name"] for i in build]
        })

        rank += 1

    return results
