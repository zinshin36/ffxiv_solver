import traceback
import sys
import time

print("BOOT: starting main.py")

try:
    from engine.logger import init_logger, log
    print("BOOT: logger imported")

    from gui.app import main as gui_main
    print("BOOT: GUI imported")

    def main():
        init_logger()
        log("Application starting (GUI mode)...")
        gui_main()

    if __name__ == "__main__":
        main()

except Exception:
    print("\n=== CRASH DETECTED (MAIN) ===")
    traceback.print_exc()

    try:
        print("\nClosing in 10 seconds...")
        time.sleep(10)
    except:
        pass
