import sys
import traceback
from engine.logger import log
from engine.food import load_foods
from engine.data_loader import load_items, load_materia

def main():
    try:
        log("[GUI] Starting application")

        # Load foods
        foods = load_foods()
        if not foods:
            log("[GUI] Warning: No foods loaded")

        # Load items
        items = load_items()
        if not items:
            log("[GUI] Warning: No items loaded")

        # Load materia
        materia = load_materia()
        if not materia:
            log("[GUI] Warning: No materia loaded")

        log(f"[GUI] Loaded {len(foods)} foods, {len(items)} items, {len(materia)} materia")

        # Initialize GUI here (pseudo, depends on your GUI framework)
        log("[GUI] GUI Ready")
        # Example: start_main_window(foods, items, materia)

    except Exception as e:
        log("[CRASH DETECTED]")
        log(f"Exception: {e}")
        log(traceback.format_exc())
        sys.exit(1)

if __name__ == "__main__":
    main()
