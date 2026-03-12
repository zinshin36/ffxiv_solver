import os
import sys

def get_base_dir():
    """Return the folder where the EXE/script is launched."""
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(sys.argv[0]))

BASE_DIR = get_base_dir()
GAME_DATA_DIR = os.path.join(BASE_DIR, "game_data")
LOG_DIR = os.path.join(BASE_DIR, "logs")
