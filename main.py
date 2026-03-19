import traceback
import sys
import os


def write_crash(e):
    try:
        os.makedirs("logs", exist_ok=True)
        with open("logs/crash.txt", "w", encoding="utf-8") as f:
            f.write("=== CRASH DETECTED ===\n\n")
            f.write(traceback.format_exc())
    except Exception:
        pass


print("BOOT: starting EXE")

try:
    print("BOOT: importing GUI...")
    from gui.app import main

    print("BOOT: launching GUI...")
    main()

except Exception as e:
    print("\n=== HARD CRASH ===")
    traceback.print_exc()

    write_crash(e)

    try:
        input("\nPress Enter to exit...")
    except Exception:
        pass
