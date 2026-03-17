from engine.logger import log
from engine.dps import calculate_score

MAX_PER_SLOT = 5

VALID_SLOTS = [
    "weapon", "head", "body", "hands",
    "legs", "feet", "earrings",
    "necklace", "bracelet", "ring"
]


def normalize_slot(slot):

    if not slot:
        return None

    s = str(slot).lower()

    # Weapons
    if "mainhand" in s or "weapon" in s:
        return "weapon"

    # Armor
    if "head" in s:
        return "head"
    if "body" in s or "chest" in s:
        return "body"
    if "hand" in s and "mainhand" not in s:
        return "hands"
    if "leg" in s:
        return "legs"
    if "feet" in s or "foot" in s:
        return "feet"

    # Accessories
    if "ear" in s:
        return "earrings"
    if "neck" in s:
        return "necklace"
    if "wrist" in s or "brace" in s:
        return "bracelet"
    if "finger" in s or "ring" in s:
        return "ring"

    return None


def group_slots(items):

    slots = {k: [] for k in VALID_SLOTS}

    for item in items:

        slot = normalize_slot(item.get("slot"))

        if not slot:
            continue

        slots[slot].append(item)

    # DEBUG OUTPUT
    for s in VALID_SLOTS:
        log(f"{s}: {len(slots[s])} items")

    return slots


def trim_slots(slots):

    for slot in slots:

        slots[slot].sort(
            key=lambda x: x.get("crit", 0)
                        + x.get("dh", 0)
                        + x.get("det", 0)
                        + x.get("sps", 0),
            reverse=True
        )

        slots[slot] = slots[slot][:MAX_PER_SLOT]


def solve(items, gcd_target, progress=None):

    log("Starting solver")

    slots = group_slots(items)

    trim_slots(slots)

    slot_order = [
        "weapon", "head", "body", "hands",
        "legs", "feet", "earrings",
        "necklace", "bracelet", "ring", "ring"
    ]

    slot_items = []

    for s in slot_order:

        if not slots[s]:
            log(f"Missing slot: {s}")
            return None, 0

        slot_items.append(slots[s])

    total = 1
    for s in slot_items:
        total *= len(s)

    log(f"Total combinations: {total}")

    best_score = 0
    best_build = None

    checked = 0

    def dfs(i, stats, build):

        nonlocal best_score, best_build, checked

        if i == len(slot_items):

            checked += 1

            score = calculate_score(stats, gcd_target)

            if score > best_score:
                best_score = score
                best_build = build.copy()
                log(f"New best {round(score, 2)}")

            if checked % 1000 == 0:
                log(f"Progress {checked}/{total}")
                if progress:
                    progress(int((checked / total) * 100))

            return

        for item in slot_items[i]:

            new_stats = stats.copy()

            for s in ["crit", "dh", "det", "sps"]:
                new_stats[s] = new_stats.get(s, 0) + item.get(s, 0)

            build.append(item)

            dfs(i + 1, new_stats, build)

            build.pop()

    dfs(0, {}, [])

    log(f"Finished. Checked {checked}")

    return best_build, best_score
