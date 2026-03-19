import threading
import tkinter as tk
from tkinter import ttk

from engine.optimizer import run_solver
from engine.data_loader import load_items, load_materia
from engine.food import load_foods


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("FFXIV BiS Solver")

        self.log_box = tk.Text(root, height=25, width=120)
        self.log_box.pack(padx=10, pady=10)

        controls = ttk.Frame(root)
        controls.pack(pady=5)

        ttk.Label(controls, text="GCD Target").grid(row=0, column=0)
        self.gcd_entry = ttk.Entry(controls)
        self.gcd_entry.insert(0, "2.2")
        self.gcd_entry.grid(row=0, column=1)

        ttk.Label(controls, text="Min iLvl").grid(row=0, column=2)
        self.ilvl_entry = ttk.Entry(controls)
        self.ilvl_entry.insert(0, "780")
        self.ilvl_entry.grid(row=0, column=3)

        ttk.Button(controls, text="Run Solver", command=self.start_solver).grid(row=0, column=4, padx=10)

        self.log("GUI Ready")

        # Load static systems
        self.log("Loading systems...")
        self.foods = load_foods(self.log)
        self.log(f"[INIT] Foods loaded: {len(self.foods)}")

    # =========================
    # LOGGING (THREAD SAFE)
    # =========================

    def log(self, msg):
        def write():
            self.log_box.insert(tk.END, msg + "\n")
            self.log_box.see(tk.END)

        self.root.after(0, write)

    # =========================
    # SOLVER THREAD
    # =========================

    def start_solver(self):
        thread = threading.Thread(target=self.run_solver)
        thread.start()

    def run_solver(self):
        try:
            gcd = float(self.gcd_entry.get())
            min_ilvl = int(self.ilvl_entry.get())

            self.log(f"Running solver | GCD={gcd} | Min iLvl={min_ilvl}")

            # Load data
            items_by_slot = load_items(min_ilvl, self.log)
            materia_csv = load_materia(self.log)

            config = {
                "gcd_target": gcd
            }

            results = run_solver(items_by_slot, materia_csv, config, self.log)

            if not results:
                self.log("[RESULT] No valid gear sets found")
                return

            self.display_results(results)

        except Exception as e:
            self.log(f"[ERROR] {e}")

    # =========================
    # DISPLAY RESULTS
    # =========================

    def display_results(self, results):
        self.log("=== TOP RESULTS ===")

        for i, entry in enumerate(results):
            build = entry["build"]
            result = entry["result"]

            self.log("")
            self.log(f"--- Build #{i+1} ---")
            self.log(f"GCD: {round(result['gcd'], 3)}")
            self.log(f"DPS: {result['dps']}")
            self.log(f"Score: {result['score']}")

            # Gear
            for slot, item in build.items():
                name = item.get("Name", "Unknown")
                self.log(f"{slot:>10}: {name}")

                # ✅ SHOW MATERIA
                mats = result.get("materia", {}).get(slot, [])

                if mats:
                    for m in mats:
                        self.log(f"            + Materia -> Param {m['param']} | +{m['value']}")
                else:
                    self.log(f"            (no materia)")

            self.log("-" * 50)


# =========================
# MAIN
# =========================

def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
