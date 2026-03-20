import threading
import traceback
import tkinter as tk
from tkinter import ttk

from engine.logger import log, init_logger, set_widget
from engine.food import load_foods
from engine.data_loader import load_items
from engine.optimizer import run_solver
from engine.blacklist import load_blacklist


# -------------------------
# GROUP BY SLOT (FIXED)
# -------------------------
def group_by_slot(items):
    slots = {}

    for item in items:
        slot = item["slot"]

        # allow 2 rings
        if slot == "ring":
            slots.setdefault("ring1", []).append(item)
            slots.setdefault("ring2", []).append(item)
        else:
            slots.setdefault(slot, []).append(item)

    return slots


# -------------------------
# APPLY FOOD
# -------------------------
def apply_food(stats, food):
    if not food:
        return stats

    result = stats.copy()

    for stat, (pct, cap) in food.get("bonus", {}).items():
        base = result.get(stat, 0)
        bonus = min(int(base * pct), cap)
        result[stat] = base + bonus

    return result


# -------------------------
# GUI
# -------------------------
class App:

    def __init__(self, root):
        self.root = root
        self.root.title("FFXIV Gear Solver")

        frame = ttk.Frame(root, padding=10)
        frame.pack(fill="both", expand=True)

        # -------------------------
        # INPUTS
        # -------------------------
        ttk.Label(frame, text="Min iLvl:").grid(row=0, column=0)
        self.ilvl_entry = ttk.Entry(frame)
        self.ilvl_entry.insert(0, "780")
        self.ilvl_entry.grid(row=0, column=1)

        ttk.Label(frame, text="Target GCD:").grid(row=1, column=0)
        self.gcd_entry = ttk.Entry(frame)
        self.gcd_entry.insert(0, "2.38")
        self.gcd_entry.grid(row=1, column=1)

        ttk.Label(frame, text="Food:").grid(row=2, column=0)

        self.food_var = tk.StringVar()
        self.food_dropdown = ttk.Combobox(frame, textvariable=self.food_var, state="readonly")
        self.food_dropdown.grid(row=2, column=1)

        self.run_btn = ttk.Button(frame, text="Run Solver", command=self.start_solver)
        self.run_btn.grid(row=3, column=0, columnspan=2, pady=5)

        self.log_box = tk.Text(frame, height=25, width=100)
        self.log_box.grid(row=4, column=0, columnspan=2)

        init_logger(self.log_box)
        set_widget(self.log_box)

        # -------------------------
        # LOAD DATA
        # -------------------------
        log("[GUI] Starting application")

        self.foods = load_foods()
        log(f"[INIT] Foods loaded: {len(self.foods)}")

        self.food_map = {f["name"]: f for f in self.foods}
        self.food_dropdown["values"] = ["None"] + list(self.food_map.keys())
        self.food_dropdown.current(0)

        self.items = load_items(min_ilvl=0)
        log(f"[INIT] Items loaded: {len(self.items)}")

        self.max_ilvl = max(i["ilvl"] for i in self.items)
        log(f"[INIT] Max iLvl detected: {self.max_ilvl}")

        self.blacklist = load_blacklist()
        log(f"[INIT] Blacklist loaded: {len(self.blacklist)} entries")

        log("[GUI] Ready")

    # -------------------------
    # THREAD
    # -------------------------
    def start_solver(self):
        t = threading.Thread(target=self.run_solver)
        t.start()

    def run_solver(self):
        try:
            min_ilvl = int(self.ilvl_entry.get())
            target_gcd = float(self.gcd_entry.get())
            food_name = self.food_var.get()

            selected_food = self.food_map.get(food_name)

            log(f"[RUN] Min iLvl={min_ilvl} | GCD={target_gcd} | Food={food_name}")

            # -------------------------
            # FILTER
            # -------------------------
            filtered = []

            for i in self.items:
                if i["ilvl"] < min_ilvl:
                    continue

                name = i["name"].lower()

                if any(b in name for b in self.blacklist):
                    continue

                filtered.append(i)

            log(f"[FILTER] Items after filter: {len(filtered)}")

            # -------------------------
            # GROUP
            # -------------------------
            items_by_slot = group_by_slot(filtered)

            for slot, arr in items_by_slot.items():
                log(f"[SLOT] {slot}: {len(arr)} items")

            # -------------------------
            # SOLVER (FIXED CALL)
            # -------------------------
            results = run_solver(items_by_slot, target_gcd, log)

            # -------------------------
            # APPLY FOOD TO RESULTS
            # -------------------------
            for r in results:
                stats = r["result"]["stats"]
                r["result"]["stats"] = apply_food(stats, selected_food)

            # -------------------------
            # OUTPUT
            # -------------------------
            log("\n=== TOP 3 BUILDS ===")

            for idx, r in enumerate(results[:3]):

                log(f"\n--- Build #{idx+1} ---")
                log(f"GCD: {r['result']['gcd']}")
                log(f"DPS: {r['result']['dps']}")
                log(f"Score: {r['result']['score']}")

                for slot, item in r["build"].items():
                    log(f"{slot:>10}: {item['name']}")

                log("  --- MATERIA ---")
                for m in r["result"]["melds"]:
                    if m["melds"]:
                        log(f"  {m['item']}: {', '.join(m['melds'])}")

            log("\n[DONE]")

        except Exception as e:
            log("[CRASH DETECTED]")
            log(str(e))
            log(traceback.format_exc())


def main():
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
