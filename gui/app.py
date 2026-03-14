import tkinter as tk

from engine.csv_loader import load_items, load_materia
from engine.optimizer import top_sets
from engine.logger import log


class SolverGUI:

    def __init__(self, root):

        root.title("BLM Gear Solver")

        frame = tk.Frame(root, padx=10, pady=10)
        frame.pack()

        tk.Label(frame, text="Target GCD").grid(row=0, column=0)

        self.gcd_entry = tk.Entry(frame)
        self.gcd_entry.insert(0, "2.38")
        self.gcd_entry.grid(row=0, column=1)

        run = tk.Button(frame, text="Run Solver", command=self.run)
        run.grid(row=1, column=0, columnspan=2)

        log("Application started")

    def run(self):

        try:
            target = float(self.gcd_entry.get())
        except:
            target = None

        log(f"Target GCD: {target}")

        items = load_items()
        materia = load_materia()

        top_sets(items, materia, target)


def main():

    root = tk.Tk()

    SolverGUI(root)

    root.mainloop()


if __name__ == "__main__":
    main()
