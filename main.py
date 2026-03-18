import os
from engine.data_parser import load_items
from engine.optimizer import solve
from engine.logger import log


def main():
    log("Application started")
    log("Loading game data...")

    items = load_items()

    # ===== FILTER =====
    MIN_ILVL = 780
    TARGET_GCD = 2.2

    filtered = [i for i in items if i["ilvl"] >= MIN_ILVL]

    log(f"Min ilvl: {MIN_ILVL}")
    log(f"GCD target: {TARGET_GCD}")
    log(f"Items after filter: {len(filtered)}")

    # ===== FOOD (basic for now) =====
    foods = [
        {"name": "None"},
        {"name": "Crit Food", "crit": 100},
        {"name": "SPS Food", "sps": 100},
        {"name": "Det Food", "det": 100}
    ]

    log("Starting solver...")

    results = solve(
        filtered,
        target_gcd=TARGET_GCD,
        foods=foods
    )

    log("\n=== TOP BUILDS ===")

    for i, build in enumerate(results, 1):
        log(f"\n--- Build #{i} ---")
        log(f"Score: {build['score']:.2f}")
        log(f"Food: {build['food']}")

        for item in build["build"]:
            log(item["name"])

        log("Materia:")
        for m in build["melds"]:
            log(f"{m['item']} -> {', '.join(m['melds'])}")

        log(f"Stats: {build['stats']}")


if __name__ == "__main__":
    main()
