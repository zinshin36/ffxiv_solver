import sys
import traceback

from engine.logger import log, init_logger
from engine.food import load_foods
from engine.data_loader import load_items, load_materia


def main():
    try:
        # -------------------------
        # INIT LOGGER (CRITICAL)
        # -------------------------
        init_logger()

        log("[GUI] Starting application")

        # -------------------------
        # LOAD FOODS (OPTIONAL)
        # -------------------------
        foods = load_foods()
        log(f"[INIT] Foods loaded: {len(foods)}")

        # -------------------------
        # LOAD ALL ITEMS (NO FILTER)
        # -------------------------
        items = load_items(min_ilvl=0)
        log(f"[INIT] Items loaded: {len(items)}")

        # -------------------------
        # DETECT MAX ILVL
        # -------------------------
        max_ilvl = 0
        for item in items:
            if item["ilvl"] > max_ilvl:
                max_ilvl = item["ilvl"]

        log(f"[INIT] Max iLvl detected: {max_ilvl}")

        # -------------------------
        # LOAD MATERIA
        # -------------------------
        materia = load_materia()
        log(f"[INIT] Materia loaded: {len(materia)}")

        # -------------------------
        # READY STATE (NO CRASH)
        # -------------------------
        log("[GUI] GUI Ready")

        # ❗ DO NOTHING ELSE
        # No input()
        # No solver auto-run
        # No blocking calls

        # Keep app alive (important for EXE)
        import time
        while True:
            time.sleep(1)

    except Exception as e:
        log("[CRASH DETECTED]")
        log(str(e))
        log(traceback.format_exc())
        sys.exit(1)


# REQUIRED FOR PYINSTALLER
if __name__ == "__main__":
    main()
