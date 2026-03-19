import traceback
import sys

print("BOOT: starting main.py")

try:
    from engine.data_parser import load_items
    print("BOOT: data_parser imported")

    from engine.optimizer import run_solver
    print("BOOT: optimizer imported")

    from engine.logger import log, init_logger
    print("BOOT: logger imported")

    def main():
        init_logger()

        log("Application started")

        items = load_items()
        log(f"Loaded {len(items)} items")

        run_solver(items)

    if __name__ == "__main__":
        main()

except Exception as e:
    print("\n=== CRASH DETECTED ===")
    traceback.print_exc()

    # ❗ DO NOT USE input() (breaks EXE)
    try:
        import time
        print("\nClosing in 10 seconds...")
        time.sleep(10)
    except:
        pass
