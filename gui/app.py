import sys
import traceback

# DO NOT import anything risky at top level
# (this is what was crashing your exe silently)

def safe_imports():
    try:
        from engine.logger import log
    except Exception:
        def log(msg):
            print(msg)

    try:
        from engine.food import load_foods
    except Exception as e:
        log(f"[IMPORT ERROR] food: {e}")
        load_foods = lambda: []

    try:
        from engine.data_loader import load_items, load_materia
    except Exception as e:
        log(f"[IMPORT ERROR] data_loader: {e}")
        load_items = lambda *args, **kwargs: []
        load_materia = lambda: []

    return log, load_foods, load_items, load_materia


def main():
    log, load_foods, load_items, load_materia = safe_imports()

    try:
        log("[GUI] Starting application")

        # -------------------------
        # LOAD SYSTEMS
        # -------------------------
        foods = load_foods()
        log(f"[INIT] Foods loaded: {len(foods)}")

        items = load_items()
        log(f"[INIT] Items loaded: {len(items)}")

        materia = load_materia()
        log(f"[INIT] Materia loaded: {len(materia)}")

        log("[GUI] GUI Ready")

        # Keep app alive (prevents instant exit in EXE)
        input("Press Enter to exit...")

    except Exception as e:
        log("[CRASH DETECTED]")
        log(str(e))
        log(traceback.format_exc())

        try:
            input("Press Enter to exit...")
        except Exception:
            pass


# IMPORTANT: this must exist for import
if __name__ == "__main__":
    main()
