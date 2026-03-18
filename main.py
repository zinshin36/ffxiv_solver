import traceback
import sys

print("BOOT: starting main.py")

try:
    from engine.data_parser import load_items
    print("BOOT: data_parser imported")

    from engine.optimizer import run_solver
    print("BOOT: optimizer imported")

    from engine.logger import log
    print("BOOT: logger imported")

    def main():
        log("Application started")

        items = load_items()
        log(f"Loaded {len(items)} items")

        run_solver(items)

    if __name__ == "__main__":
        main()

except Exception as e:
    print("\n=== CRASH DETECTED ===")
    traceback.print_exc()
    input("\nPress Enter to exit...")
