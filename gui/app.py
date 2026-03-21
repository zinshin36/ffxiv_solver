import tkinter as tk
from tkinter import ttk, messagebox
import os
from engine.optimizer import run_solver
from engine.data_loader import load_items
from engine.food_system import load_foods

BLACKLIST_FILE = "blacklist.txt"

class App:
    def __init__(self, root, items_by_slot):
        self.root = root
        self.root.title("FFXIV BIS Solver")
        self.items_by_slot = items_by_slot
        self.foods = load_foods()
        self.blacklist = self.load_blacklist()
        self.build_type = tk.StringVar(value="Crit")

        self.min_ilvl = tk.IntVar(value=0)
        self.gcd = tk.DoubleVar(value=2.5)
        self.selected_food = tk.StringVar()
        if self.foods:
            self.selected_food.set(self.foods[0]['name'])

        self.create_gui()

    def load_blacklist(self):
        if os.path.exists(BLACKLIST_FILE):
            with open(BLACKLIST_FILE, "r") as f:
                return set(line.strip() for line in f if line.strip())
        return set()

    def create_gui(self):
        frame = ttk.Frame(self.root)
        frame.pack(padx=10, pady=10)

        ttk.Label(frame, text="Min iLvl:").grid(row=0, column=0, sticky="w")
        ttk.Entry(frame, textvariable=self.min_ilvl).grid(row=0, column=1)

        ttk.Label(frame, text="Target GCD:").grid(row=1, column=0, sticky="w")
        ttk.Entry(frame, textvariable=self.gcd).grid(row=1, column=1)

        ttk.Label(frame, text="Food:").grid(row=2, column=0, sticky="w")
        food_menu = ttk.OptionMenu(frame, self.selected_food, self.selected_food.get(),
                                   *[f['name'] for f in self.foods])
        food_menu.grid(row=2, column=1)

        ttk.Label(frame, text="Build Type:").grid(row=3, column=0, sticky="w")
        ttk.OptionMenu(frame, self.build_type, self.build_type.get(), "Crit", "Spell Speed").grid(row=3, column=1)

        run_btn = ttk.Button(frame, text="Run Solver", command=self.run_solver_gui)
        run_btn.grid(row=4, column=0, columnspan=2, pady=10)

        self.log = tk.Text(self.root, height=25, width=100)
        self.log.pack()

    def log_msg(self, msg):
        self.log.insert(tk.END, f"{msg}\n")
        self.log.see(tk.END)
        self.root.update_idletasks()

    def run_solver_gui(self):
        if not self.items_by_slot:
            messagebox.showerror("Error", "No items loaded.")
            return
        # get selected food dict
        food = next((f for f in self.foods if f['name'] == self.selected_food.get()), None)

        self.log_msg(f"[RUN] Min iLvl={self.min_ilvl.get()} | GCD={self.gcd.get()} | Food={self.selected_food.get()} | Build Type={self.build_type.get()}")
        filtered_items = self.filter_items()
        self.log_msg(f"[FILTER] Items after filter: {sum(len(v) for v in filtered_items.values())}")
        for slot, items in filtered_items.items():
            self.log_msg(f"[SLOT] {slot}: {len(items)} items")

        try:
            results = run_solver(
                items_by_slot=filtered_items,
                min_ilvl=self.min_ilvl.get(),
                target_gcd=self.gcd.get(),
                build_type=self.build_type.get(),
                selected_food=food,
                blacklist=self.blacklist,
            )
            self.display_results(results)
        except Exception as e:
            self.log_msg(f"[CRASH DETECTED]\n{e}")

    def filter_items(self):
        filtered = {}
        for slot, items in self.items_by_slot.items():
            filtered[slot] = [i for i in items if i['name'] not in self.blacklist and i['ilvl'] >= self.min_ilvl.get()]
        return filtered

    def display_results(self, builds):
        self.log_msg("===== RESULTS =====")
        for i, build in enumerate(builds, 1):
            self.log_msg(f"\n=== BUILD {i} ===")
            self.log_msg(f"DPS: {build['dps']:.2f}")
            self.log_msg(f"GCD: {build['gcd']:.3f}")
            self.log_msg(f"CRIT: {build['crit']}  DH: {build['dh']}  DET: {build['det']}  SPS: {build['sps']}")
            for slot in ["weapon","head","body","hands","legs","feet","earrings","necklace","bracelet","ring1","ring2"]:
                item = build['items'].get(slot)
                if item:
                    self.log_msg(f"{slot}: {item['name']}")
                    if item.get('melds'):
                        melds = ', '.join([f"{k}+{v}" for k,v in item['melds'].items()])
                        self.log_msg(f"  melds: {melds}")

def main(items_by_slot=None):
    if items_by_slot is None:
        items_by_slot = load_items()
    root = tk.Tk()
    app = App(root, items_by_slot)
    root.mainloop()

if __name__ == "__main__":
    main()
