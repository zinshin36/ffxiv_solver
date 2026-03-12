import tkinter as tk
from gui.app import App
from engine.logger import setup_logger

def main():
    setup_logger()
    root = tk.Tk()
    App(root)
    root.mainloop()

if __name__ == "__main__":
    main()
