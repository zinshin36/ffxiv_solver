import tkinter as tk
from tkinter import ttk
from engine.data_loader import load_items
from engine.optimizer import run_solver
from engine.food_system import load_foods

SLOTS = [
    "weapon","head","body","hands","legs",
    "feet","earrings","necklace","bracelet","ring1","ring2"
]

def build_items_by_slot(items):
    slots = {s: [] for s in SLOTS}

    for item in items:
        slot = item["slot"]

        if slot == "ring":
            slots["ring1"].append(item)
            slots["ring2"].append(item)
        elif slot in slots:
            slots[slot].append(item)

    return slots


class App:

    def __init__(self, root):

        self.root = root
        self.root.title("FFXIV BIS Solver")

        self.items = load_items()
        self.items_by_slot = build_items_by_slot(self.items)
        self.foods = load_foods()

        self.gcd = tk.DoubleVar(value=2.5)
        self.build_type = tk.StringVar(value="Crit")
        self.food = tk.StringVar(value=self.foods[0]["name"] if self.foods else "None")

        self.create_ui()

    def create_ui(self):

        frame = ttk.Frame(self.root)
        frame.pack(padx=10, pady=10)

        ttk.Label(frame, text="Target GCD").grid(row=0, column=0)
        ttk.Entry(frame, textvariable=self.gcd).grid(row=0, column=1)

        ttk.Label(frame, text="Build Type").grid(row=1, column=0)
        ttk.OptionMenu(frame, self.build_type, "Crit", "Crit", "Spell Speed").grid(row=1, column=1)

        ttk.Label(frame, text="Food").grid(row=2, column=0)
        ttk.OptionMenu(frame, self.food, self.food.get(), *[f["name"] for f in self.foods]).grid(row=2, column=1)

        ttk.Button(frame, text="Solve", command=self.solve).grid(row=3, column=0, columnspan=2)

        self.output = tk.Text(self.root, width=100, height=30)
        self.output.pack()

    def log(self, msg):
        self.output.insert("end", msg + "\n")
        self.output.see("end")

    def solve(self):

        self.output.delete("1.0", tk.END)

        results = run_solver(
            self.items_by_slot,
            target_gcd=self.gcd.get(),
            build_type=self.build_type.get(),
            selected_food=self.food.get(),
            foods=self.foods
        )

        for i, b in enumerate(results, 1):
            self.log(f"\n=== BUILD {i} ===")
            self.log(f"DPS: {b['dps']:.2f} | GCD: {b['gcd']:.3f}")
            self.log(f"CRIT:{b['crit']} DH:{b['dh']} DET:{b['det']} SPS:{b['sps']}")

            for slot in SLOTS:
                item = b["items"][slot]
                self.log(f"{slot}: {item['name']}")

                if item.get("melds"):
                    melds = ", ".join([f"{k}+{v}" for k,v in item["melds"].items()])
                    self.log(f"  melds: {melds}")


def main():
    root = tk.Tk()
    App(root)
    root.mainloop()
