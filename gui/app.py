import tkinter as tk

from engine.csv_loader import load_items, load_materia
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

        run = tk.Button(frame, text="Run Solver", command=self.run)
        run.grid(row=1, column=0, columnspan=2)

    def run(self):

        try:
            target = float(self.gcd.get())
        except:
            target = None

        log("Solver started")

        items = load_items()
        materia = load_materia()

        solve(items, materia, target)


def main():

    root = tk.Tk()

    App(root)

    root.mainloop()


if __name__ == "__main__":
    main()
