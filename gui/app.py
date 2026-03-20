import tkinter as tk
from tkinter import ttk
import traceback

from engine.logger import init_logger, log
from engine.food import load_foods
from engine.data_loader import load_items
from engine.blacklist import load_blacklist
from engine.optimizer import run_solver


class App:

    def __init__(self, root):
        self.root = root
        self.root.title("FFXIV BIS Solver")

        # -------------------------
        # UI VARIABLES
        # -------------------------
        self.min_ilvl_var = tk.StringVar()
        self.gcd_var = tk.StringVar()
        self.food_var = tk.StringVar()

        # -------------------------
        # TOP CONTROLS
        # -------------------------
        frame = ttk.Frame(root)
        frame.pack(padx=10, pady=10, fill="x")

        ttk.Label(frame, text="Min iLvl").grid(row=0, column=0)
        ttk.Entry(frame, textvariable=self.min_ilvl_var, width=10).grid(row=0, column=1)

        ttk.Label(frame, text="Target GCD (optional)").grid(row=0, column=2)
        ttk.Entry(frame, textvariable=self.gcd_var, width=10).grid(row=0, column=3)

        ttk.Label(frame, text="Food").grid(row=0, column=4)
        self.food_dropdown = ttk.Combobox(frame, textvariable=self.food_var, width=25)
        self.food_dropdown.grid(row=0, column=5)

        ttk.Button(frame, text="Detect Max iLvl", command=self.detect_max_ilvl).grid(row=1, column=0, columnspan=2, pady=5)
        ttk.Button(frame, text="Run Solver", command=self.run).grid(row=1, column=2, columnspan=2, pady=5)

        # -------------------------
        # LOG OUTPUT
        # -------------------------
        self.text = tk.Text(root, height=30)
        self.text.pack(fill="both", expand=True)

        init_logger(self.text)

        # -------------------------
        # LOAD DATA
        # -------------------------
        self.init_data()

    # -------------------------
    # LOAD EVERYTHING
    # -------------------------
    def init_data(self):
        try:
            log("[GUI] Starting application")

            self.foods = load_foods()
            self.items = load_items()
            self.blacklist = load_blacklist()

            self.max_ilvl = max(i["ilvl"] for i in self.items) if self.items else 0

            log(f"[INIT] Foods loaded: {len(self.foods)}")
            log(f"[INIT] Items loaded: {len(self.items)}")
            log(f"[INIT] Max iLvl detected: {self.max_ilvl}")
            log(f"[INIT] Blacklist loaded: {len(self.blacklist)} entries")

            # Populate food dropdown
            food_names = ["None"] + [f["name"] for f in self.foods]
            self.food_dropdown["values"] = food_names
            self.food_dropdown.current(0)

            log("[GUI] Ready")

        except Exception as e:
            log("[CRASH DETECTED]")
            log(str(e))
            log(traceback.format_exc())

    # -------------------------
    # DETECT MAX ILVL
    # -------------------------
    def detect_max_ilvl(self):
        self.min_ilvl_var.set(str(self.max_ilvl))
        log(f"[GUI] Set Min iLvl = {self.max_ilvl}")

    # -------------------------
    # BUILD SLOT MAP
    # -------------------------
    def build_slots(self, items):

        slots = {
            "weapon": [],
            "head": [],
            "body": [],
            "hands": [],
            "legs": [],
            "feet": [],
            "earrings": [],
            "necklace": [],
            "bracelet": [],
            "ring1": [],
            "ring2": []
        }

        for item in items:

            if any(b in item["name"].lower() for b in self.blacklist):
                continue

            slot = item["slot"]

            if slot == "ring":
                slots["ring1"].append(item)
                slots["ring2"].append(item)
            elif slot in slots:
                slots[slot].append(item)

        # Debug log
        for s in slots:
            log(f"[SLOT] {s}: {len(slots[s])} items")

        return slots

    # -------------------------
    # GET FOOD STATS
    # -------------------------
    def get_food_stats(self):
        selected = self.food_var.get()

        if selected == "None":
            return None

        for f in self.foods:
            if f["name"] == selected:
                return f["bonus"]

        return None

    # -------------------------
    # RUN SOLVER
    # -------------------------
    def run(self):
        try:
            min_ilvl = int(self.min_ilvl_var.get())
        except:
            min_ilvl = 0

        try:
            target_gcd = float(self.gcd_var.get())
        except:
            target_gcd = None

        food = self.get_food_stats()

        log(f"[RUN] Min iLvl={min_ilvl} | GCD={target_gcd} | Food={self.food_var.get()}")

        # -------------------------
        # FILTER ITEMS
        # -------------------------
        filtered = [i for i in self.items if i["ilvl"] >= min_ilvl]

        log(f"[FILTER] Items after filter: {len(filtered)}")

        slots = self.build_slots(filtered)

        # -------------------------
        # SOLVE
        # -------------------------
        results = run_solver(slots, food, target_gcd, log)

        # -------------------------
        # DISPLAY RESULTS
        # -------------------------
        log("\n===== RESULTS =====\n")

        for i, res in enumerate(results, 1):

            r = res["result"]
            build = res["build"]

            stats = r["stats"]

            log(f"=== BUILD {i} ===")
            log(f"DPS: {r['dps']:.2f}")
            log(f"GCD: {r['gcd']:.3f}")
            log(f"CRIT: {stats['crit']}  DH: {stats['dh']}  DET: {stats['det']}  SPS: {stats['sps']}")
            log("")

            for slot in build:
                item = build[slot]
                melds = r["melds"].get(slot, [])

                log(f"{slot}: {item['name']}")

                if melds:
                    log(f"  melds: {', '.join(melds)}")

            log("")

    # -------------------------
    # START
    # -------------------------
def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
