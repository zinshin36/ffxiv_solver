import tkinter as tk
from tkinter import ttk
import traceback

from engine.logger import log, init_logger
from engine.food import load_foods
from engine.data_loader import load_items
from engine.blacklist import load_blacklist
from engine.optimizer import run_solver


class App:

    def __init__(self, root):
        self.root = root
        self.root.title("FFXIV BLM BiS Solver")

        # -------------------------
        # UI VARIABLES
        # -------------------------
        self.min_ilvl_var = tk.StringVar(value="0")
        self.gcd_var = tk.StringVar(value="")
        self.food_var = tk.StringVar()

        # -------------------------
        # LAYOUT
        # -------------------------
        frame = ttk.Frame(root, padding=10)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Min iLvl:").grid(row=0, column=0, sticky="w")
        ttk.Entry(frame, textvariable=self.min_ilvl_var, width=10).grid(row=0, column=1)

        ttk.Label(frame, text="Target GCD (optional):").grid(row=1, column=0, sticky="w")
        ttk.Entry(frame, textvariable=self.gcd_var, width=10).grid(row=1, column=1)

        ttk.Label(frame, text="Food:").grid(row=2, column=0, sticky="w")
        self.food_dropdown = ttk.Combobox(frame, textvariable=self.food_var, state="readonly")
        self.food_dropdown.grid(row=2, column=1, sticky="ew")

        ttk.Button(frame, text="Run Solver", command=self.run_solver).grid(row=3, column=0, columnspan=2, pady=5)

        self.log_box = tk.Text(frame, height=25, width=80)
        self.log_box.grid(row=4, column=0, columnspan=2, pady=5)

        frame.columnconfigure(1, weight=1)

        # -------------------------
        # INIT LOGGER
        # -------------------------
        init_logger(self.log_box)

        log("[GUI] Starting application")

        # -------------------------
        # LOAD DATA
        # -------------------------
        self.foods = load_foods()
        log(f"[INIT] Foods loaded: {len(self.foods)}")

        self.items = load_items()
        log(f"[INIT] Items loaded: {len(self.items)}")

        self.max_ilvl = max(x["ilvl"] for x in self.items) if self.items else 0
        log(f"[INIT] Max iLvl detected: {self.max_ilvl}")

        self.blacklist = load_blacklist()
        log(f"[INIT] Blacklist loaded: {len(self.blacklist)} entries")

        # -------------------------
        # FOOD DROPDOWN
        # -------------------------
        food_names = ["None"] + [f["name"] for f in self.foods]
        self.food_dropdown["values"] = food_names

        if food_names:
            self.food_var.set(food_names[0])

        log("[GUI] Ready")

    # -------------------------
    # CONVERT FOOD TO BONUS
    # -------------------------
    def get_food_bonus(self, food_name):
        if food_name == "None":
            return {}

        for f in self.foods:
            if f["name"] == food_name:
                return f["bonus"]

        return {}

    # -------------------------
    # SOLVER
    # -------------------------
    def run_solver(self):
        try:
            min_ilvl = int(self.min_ilvl_var.get() or 0)

            target_gcd = 2.50
            if self.gcd_var.get().strip():
                target_gcd = float(self.gcd_var.get())

            selected_food = self.food_var.get()
            food_bonus = self.get_food_bonus(selected_food)

            log(f"[RUN] Min iLvl={min_ilvl} | GCD={target_gcd} | Food={selected_food}")

            # -------------------------
            # FILTER ITEMS
            # -------------------------
            filtered = [
                x for x in self.items
                if x["ilvl"] >= min_ilvl
                and not any(b in x["name"].lower() for b in self.blacklist)
            ]

            log(f"[FILTER] Items after filter: {len(filtered)}")

            # -------------------------
            # GROUP BY SLOT
            # -------------------------
            slots = {}
            for item in filtered:
                slot = item["slot"]

                if slot == "ring":
                    slots.setdefault("ring1", []).append(item)
                    slots.setdefault("ring2", []).append(item)
                else:
                    slots.setdefault(slot, []).append(item)

            for s in slots:
                log(f"[SLOT] {s}: {len(slots[s])} items")

            # -------------------------
            # RUN SOLVER (FIXED CALL)
            # -------------------------
            results = run_solver(
                items_by_slot=slots,
                target_gcd=target_gcd,
                food_bonus=food_bonus,
                logger=log
            )

            # -------------------------
            # DISPLAY RESULTS
            # -------------------------
            log("\n===== RESULTS =====\n")

            for i, r in enumerate(results[:3]):
                build = r["build"]
                res = r["result"]
                stats = res.get("stats", {})

                log(f"=== BUILD {i+1} ===")
                log(f"DPS: {res['dps']:.2f}")
                log(f"GCD: {res['gcd']:.3f}")
                log(f"CRIT: {stats.get('crit',0)}  DH: {stats.get('dh',0)}  DET: {stats.get('det',0)}  SPS: {stats.get('sps',0)}\n")

                for slot, item in build.items():
                    log(f"{slot}: {item['name']}")

                log("")

        except Exception as e:
            log("[CRASH DETECTED]")
            log(str(e))
            log(traceback.format_exc())


# -------------------------
# ENTRY POINT
# -------------------------
def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
