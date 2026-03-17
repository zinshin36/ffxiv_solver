from engine.logger import log
from engine.dps import calculate_score


TOP_PER_SLOT = 6


def group_by_slot(items):

    slots = {}

    for i in items:
        slots.setdefault(i["slot"], []).append(i)

    return slots


def trim_slots(slots):

    for slot in slots:

        slots[slot].sort(
            key=lambda x: x.get("crit",0)+x.get("dh",0)+x.get("det",0)+x.get("sps",0),
            reverse=True
        )

        slots[slot] = slots[slot][:TOP_PER_SLOT]


def solve(items, gcd_target, progress=None):

    log("Starting solver")

    slots = group_by_slot(items)

    trim_slots(slots)

    slot_list = list(slots.values())

    best_score = 0
    best_build = None

    checked = 0


    def dfs(i, stats, build):

        nonlocal best_score, best_build, checked

        if i >= len(slot_list):

            checked += 1

            score = calculate_score(stats, gcd_target)

            if score > best_score:

                best_score = score
                best_build = build.copy()

                log(f"New best score {round(score,2)}")

            if checked % 2000 == 0 and progress:
                progress(checked)

            return


        for item in slot_list[i]:

            new_stats = stats.copy()

            for s in ["crit","dh","det","sps"]:
                new_stats[s] = new_stats.get(s,0) + item.get(s,0)

            build.append(item)

            dfs(i+1,new_stats,build)

            build.pop()


    dfs(0,{},[])

    log(f"Solver checked {checked} builds")

    return best_build, best_score
