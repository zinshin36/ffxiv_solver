from engine.logger import log


def solve(items, progress_callback=None):

    log("Solve() called")

    # group by slot
    slots = {}

    for item in items:

        slot = item["slot"]

        if slot not in slots:
            slots[slot] = []

        slots[slot].append(item)

    slot_list = list(slots.values())

    best = []
    checked = 0

    def dfs(slot_index, build):

        nonlocal checked

        if slot_index >= len(slot_list):

            checked += 1

            if checked % 5000 == 0:
                log(f"Checked {checked} builds")

                if progress_callback:
                    progress_callback(checked)

            best.append({
                "rank": len(best) + 1,
                "items": [i["name"] for i in build],
                "dps": sum(i["ilvl"] for i in build)
            })

            if len(best) > 20:
                best.sort(key=lambda x: x["dps"], reverse=True)
                best[:] = best[:10]

            return

        for item in slot_list[slot_index]:

            dfs(slot_index + 1, build + [item])

    log("Starting solver")

    dfs(0, [])

    log("Solver finished")

    return best
