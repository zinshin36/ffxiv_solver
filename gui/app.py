import tkinter as tk

from engine.data_parser import load_items
from engine.optimizer import run_solver
from engine.logger import log


class App:

    def __init__(self, root):

        root.title("BLM Solver")

        frame = tk.Frame(root, padx=10, pady=10)
        frame.pack()

        tk.Label(frame, text="Target GCD").grid(row=0, column=0)

        self.gcd = tk.Entry(frame)
        self.gcd.insert(0, "2.38")
        self.gcd.grid(row=0, column=1)

        tk.Button(
            frame,
            text="Run Solver",
            command=self.run
        ).grid(row=1, column=0, columnspan=2)

        log("GUI Ready")

    def run(self):
        try:
            gcd = float(self.gcd.get())

            log("Loading items...")
            items = load_items()

            log("Starting solver...")
            run_solver(items, gcd)

        except Exception as e:
            log(f"[GUI ERROR] {e}")


def main():
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
