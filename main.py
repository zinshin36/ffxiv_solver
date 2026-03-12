import tkinter as tk
import logging

from gui.app import App
from engine.logger import setup_logger
from engine.runtime_paths import BASE_DIR


def main():

    setup_logger()

    logging.info(f"Running from: {BASE_DIR}")

    root = tk.Tk()

    App(root)

    root.mainloop()


if __name__ == "__main__":
    main()
