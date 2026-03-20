import traceback
import sys
import os

# FORCE visible output EVEN IN WINDOWED MODE
def force_console():
    try:
        import ctypes
        ctypes.windll.kernel32.AllocConsole()
        sys.stdout = open("CONOUT$", "w")
        sys.stderr = open("CONOUT$", "w")
    except Exception:
        pass

force_console()

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

    # VERY SAFE IMPORT
    import importlib
    gui_module = importlib.import_module("gui.app")

    if not hasattr(gui_module, "main"):
        raise Exception("gui.app has NO main()")

    print("BOOT: launching GUI...")

    gui_module.main()

except Exception as e:
    print("\n=== HARD CRASH ===")
    traceback.print_exc()

    write_crash(e)

    try:
        input("\nPress Enter to exit...")
    except Exception:
        pass
