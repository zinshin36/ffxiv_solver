import tkinter as tk

from engine.gear_database import load_items
from engine.materia_system import load_materia
from engine.optimizer import solve
from engine.logger import log


class App:

    def __init__(self, root):

        root.title("BLM Gear Solver")

        frame = tk.Frame(root, padx=10, pady=10)
        frame.pack()

        tk.Label(frame, text="Target GCD").grid(row=0, column=0)

        self.gcd = tk.Entry(frame)
        self.gcd.insert(0, "2.38")
        self.gcd.grid(row=0, column=1)

        tk.Label(frame, text="Minimum iLvl").grid(row=1, column=0)

        self.ilvl = tk.Entry(frame)
        self.ilvl.insert(0, "650")
        self.ilvl.grid(row=1, column=1)

        tk.Label(frame, text="Food").grid(row=2, column=0)

        self.food = tk.StringVar()
        self.food.set("None")

        tk.OptionMenu(
            frame,
            self.food,
            "None",
            "Crit Food",
            "SpS Food"
        ).grid(row=2, column=1)

        tk.Button(
            frame,
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
