import sys
import traceback
from engine.logger import log

# -------------------------
# Safe imports
# -------------------------
try:
    from engine.food import load_foods
except ImportError as e:
    log(f"[IMPORT ERROR] engine.food.load_foods failed: {e}")
    load_foods = lambda: []

try:
    from engine.data_loader import load_items, load_materia
except ImportError as e:
    log(f"[IMPORT ERROR] engine.data_loader functions failed: {e}")
    load_items = lambda: []
    load_materia = lambda: []

# -------------------------
# Main GUI
# -------------------------
def main():
    try:
        log("[GUI] Starting application")

        foods = load_foods()
        if not foods:
            log("[GUI] Warning: No foods loaded")

        items = load_items()
        if not items:
            log("[GUI] Warning: No items loaded")

        materia = load_materia()
        if not materia:
            log("[GUI] Warning: No materia loaded")

        log(f"[GUI] Loaded {len(foods)} foods, {len(items)} items, {len(materia)} materia")

        log("[GUI] GUI Ready")
        # TODO: Initialize your actual GUI here

    except Exception as e:
        log("[CRASH DETECTED]")
        log(f"Exception: {e}")
        log(traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    main()
