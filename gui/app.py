import tkinter as tk

from engine.gear_database import load_items
from engine.materia_system import load_materia
from engine.optimizer import solve
from engine.logger import log


class App:

    def __init__(self, root):

        root.title("BLM Solver")

        f = tk.Frame(root, padx=10, pady=10)
        f.pack()

        tk.Label(f, text="Target GCD").grid(row=0, column=0)

        self.gcd = tk.Entry(f)
        self.gcd.insert(0, "2.38")
        self.gcd.grid(row=0, column=1)

        tk.Label(f, text="Min iLvl").grid(row=1, column=0)

        self.ilvl = tk.Entry(f)
        self.ilvl.insert(0, "650")
        self.ilvl.grid(row=1, column=1)

        tk.Label(f, text="Food").grid(row=2, column=0)

        self.food = tk.StringVar()
        self.food.set("None")

        tk.OptionMenu(f, self.food, "None", "Crit Food", "SpS Food").grid(row=2, column=1)

        tk.Button(
            f,
            text="Run Solver",
            command=self.run
        ).grid(row=3, column=0, columnspan=2)

        log("Application started")

    def run(self):

        gcd = float(self.gcd.get())
        ilvl = int(self.ilvl.get())

        items = load_items(ilvl)

        materia = load_materia()

        solve(items, materia, gcd, self.food.get())


def main():

    root = tk.Tk()

    App(root)

    root.mainloop()


if __name__ == "__main__":
    main()
