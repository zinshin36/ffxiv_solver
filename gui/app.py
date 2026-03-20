import sys
import traceback

def main():
    try:
        # SAFE IMPORTS INSIDE MAIN (prevents import-time crashes)
        from engine.logger import log
        from engine.food import load_foods
        from engine.data_loader import load_items, load_materia

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

        # Prevent EXE from instantly closing
        input("Press Enter to exit...")

    except Exception as e:
        try:
            from engine.logger import log
            log("[CRASH DETECTED]")
            log(str(e))
            log(traceback.format_exc())
        except Exception:
            print("[CRASH DETECTED]")
            print(str(e))
            print(traceback.format_exc())

        try:
            input("Press Enter to exit...")
        except Exception:
            pass


if __name__ == "__main__":
    main()
