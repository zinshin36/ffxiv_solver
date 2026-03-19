import tkinter as tk
import threading

from engine.data_parser import load_items
from engine.optimizer import solve, load_food
from engine.logger import init_logger, log
from engine.blacklist import load_blacklist


class App:

    def __init__(self, root):

        root.title("BLM Solver")

        frame = tk.Frame(root)
        frame.pack()

        # GCD
        tk.Label(frame, text="Target GCD").grid(row=0, column=0)
        self.gcd = tk.Entry(frame)
        self.gcd.insert(0, "2.38")
        self.gcd.grid(row=0, column=1)

        # ILVL
        tk.Label(frame, text="Min iLvl").grid(row=1, column=0)
        self.ilvl = tk.Entry(frame)
        self.ilvl.insert(0, "0")
        self.ilvl.grid(row=1, column=1)

        # FOOD
        tk.Label(frame, text="Food").grid(row=2, column=0)
        self.food_var = tk.StringVar()
        self.food_dropdown = tk.OptionMenu(frame, self.food_var, "")
        self.food_dropdown.grid(row=2, column=1)

        # BUTTONS
        tk.Button(frame, text="Detect Max iLvl", command=self.detect_ilvl).grid(row=3, column=0, columnspan=2)
        tk.Button(frame, text="Run Solver", command=self.run).grid(row=4, column=0, columnspan=2)

        # LOG BOX
        self.log_box = tk.Text(root, height=20, width=90)
        self.log_box.pack()

        init_logger(self.log_box)

        log("GUI Ready")

        self.items = []
        self.max_ilvl = 0

        # load systems immediately
        threading.Thread(target=self.load_systems).start()

    def load_systems(self):

        log("Loading systems...")

        # blacklist
        bl = load_blacklist()
        log(f"[INIT] Blacklist loaded: {len(bl)}")

        # food
        foods = load_food()

        if not foods:
            log("[FOOD] No foods loaded")
            self.food_var.set("None")
            return

        names = [f["name"] for f in foods]

        self.food_var.set(names[0])

        menu = self.food_dropdown["menu"]
        menu.delete(0, "end")

        for name in names:
            menu.add_command(label=name, command=lambda v=name: self.food_var.set(v))

        log(f"[FOOD] Dropdown populated with {len(names)} foods")

    def detect_ilvl(self):
        threading.Thread(target=self._detect_ilvl).start()

    def _detect_ilvl(self):

        log("Detecting max item level...")

        self.items, self.max_ilvl = load_items()

        log(f"[RESULT] Total items loaded: {len(self.items)}")
        log(f"[RESULT] Max iLvl detected: {self.max_ilvl}")

    def run(self):
        threading.Thread(target=self.run_solver).start()

    def run_solver(self):

        if not self.items:
            log("[ERROR] Items not loaded. Press 'Detect Max iLvl' first.")
            return

        gcd = float(self.gcd.get())
        ilvl = int(self.ilvl.get())
        food = self.food_var.get()

        log(f"Running solver | GCD={gcd} | Min iLvl={ilvl} | Food={food}")

        solve(self.items, gcd, ilvl, food)


def main():
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
