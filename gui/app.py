import sys
import traceback

# -------------------------
# SAFE IMPORTS
# -------------------------
try:
    from engine.data_loader import load_items, load_materia
except Exception as e:
    print(f"[CRITICAL] Failed to import data_loader: {e}\n{traceback.format_exc()}")
    load_items = None
    load_materia = None

try:
    from engine.food import load_foods
except Exception as e:
    print(f"[CRITICAL] Failed to import food: {e}\n{traceback.format_exc()}")
    load_foods = None

try:
    from engine.logger import log
except Exception as e:
    print(f"[CRITICAL] Failed to import logger: {e}\n{traceback.format_exc()}")
    def log(msg): print(msg)

# -------------------------
# GUI / APP LOGIC
# -------------------------
def main():
    log("[GUI] Application started")

    if load_foods:
        foods = load_foods()
        log(f"[GUI] Foods loaded: {len(foods)}")
    else:
        log("[GUI] No foods loaded")

    if load_items and load_materia:
        log("[GUI] Loading systems...")

        try:
            items = load_items()
            log(f"[GUI] {len(items)} items loaded")
        except Exception as e:
            log(f"[GUI] Failed to load items: {e}\n{traceback.format_exc()}")

        try:
            materia = load_materia()
            log(f"[GUI] Materia loaded: {len(materia)}")
        except Exception as e:
            log(f"[GUI] Failed to load materia: {e}\n{traceback.format_exc()}")

    else:
        log("[GUI] Item or Materia loader missing")

    log("[GUI] GUI Ready")
    # You can put your actual GUI init code here (Tkinter, PyQt, etc.)
    # For now, just a placeholder:
    print("GUI running... (placeholder)")

# -------------------------
# SAFE ENTRY POINT
# -------------------------
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[FATAL] Unhandled exception in main: {e}\n{traceback.format_exc()}")
        sys.exit(1)
