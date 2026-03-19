import sys
from engine.data_loader import load_items, load_materia
from engine.food import load_foods
from engine.logger import log

# -------------------------
# GUI / App Core (CLI Version)
# -------------------------
class App:
    def __init__(self):
        self.items = []
        self.materia = []
        self.foods = []

    def load_systems(self):
        log("[APP] Loading systems...")

        # Load foods
        self.foods = load_foods()

        # Load items
        self.items = load_items(min_ilvl=0)

        # Load materia
        self.materia = load_materia()

        log("[APP] Systems loaded")

    def run_solver(self):
        if not self.items:
            log("[APP] No items loaded, cannot run solver")
            return

        # Minimal placeholder solver for demo
        log(f"[SOLVER] Running with {len(self.items)} items, {len(self.materia)} materia, {len(self.foods)} foods")
        for i, item in enumerate(self.items[:5]):  # show only first 5 items for demo
            log(f"Item #{i+1}: {item['name']} | Slot: {item['slot']} | Materia slots: {item.get('materia_slots', 0)}")

# -------------------------
# Main Entry Point
# -------------------------
def main():
    log("[APP] GUI Ready")
    app = App()
    app.load_systems()
    app.run_solver()
    return app

# -------------------------
# Allow direct run
# -------------------------
if __name__ == "__main__":
    main()
