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
# GROUP BY SLOT
# -------------------------
def group_by_slot(items):
    slots = {}
    for item in items:
        slots.setdefault(item["slot"], []).append(item)
    return slots


# -------------------------
# GUI APP
# -------------------------
class App:

    def __init__(self, root):
        self.root = root
        self.root.title("FFXIV Gear Solver")

        # -------------------------
        # UI
        # -------------------------
        frame = ttk.Frame(root, padding=10)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Min iLvl:").grid(row=0, column=0, sticky="w")
        self.ilvl_entry = ttk.Entry(frame)
        self.ilvl_entry.insert(0, "780")
        self.ilvl_entry.grid(row=0, column=1)

        ttk.Label(frame, text="Target GCD:").grid(row=1, column=0, sticky="w")
        self.gcd_entry = ttk.Entry(frame)
        self.gcd_entry.insert(0, "2.38")
        self.gcd_entry.grid(row=1, column=1)

        self.run_btn = ttk.Button(frame, text="Run Solver", command=self.start_solver)
        self.run_btn.grid(row=2, column=0, columnspan=2, pady=5)

        self.log_box = tk.Text(frame, height=25, width=100)
        self.log_box.grid(row=3, column=0, columnspan=2, pady=10)

        # attach logger to GUI
        init_logger(self.log_box)
        set_widget(self.log_box)

        # -------------------------
        # LOAD DATA ON START
        # -------------------------
        log("[GUI] Starting application")

        self.foods = load_foods()
        log(f"[INIT] Foods loaded: {len(self.foods)}")

        self.items = load_items(min_ilvl=0)
        log(f"[INIT] Items loaded: {len(self.items)}")

        self.max_ilvl = max(i["ilvl"] for i in self.items)
        log(f"[INIT] Max iLvl detected: {self.max_ilvl}")

        self.blacklist = load_blacklist()
        log(f"[INIT] Blacklist loaded: {len(self.blacklist)} entries")

        log("[GUI] Ready")

    # -------------------------
    # RUN THREAD
    # -------------------------
    def start_solver(self):
        t = threading.Thread(target=self.run_solver)
        t.start()

    def run_solver(self):
        try:
            # -------------------------
            # INPUT
            # -------------------------
            min_ilvl = int(self.ilvl_entry.get())
            target_gcd = float(self.gcd_entry.get())

            log(f"[RUN] Min iLvl={min_ilvl} | Target GCD={target_gcd}")

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
            # SOLVER
            # -------------------------
            results = run_solver(items_by_slot, target_gcd, log)

            # -------------------------
            # OUTPUT TOP 3
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


# -------------------------
# ENTRY
# -------------------------
def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
