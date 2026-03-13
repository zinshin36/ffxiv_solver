# engine/logger.py
import os
from datetime import datetime

# Log everything inside the folder you are running in
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

log_file = os.path.join(LOG_DIR, f"log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")

def log(message: str):
    """
    Logs a message to the log file and prints it to the console.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"{timestamp} [INFO] {message}"
    print(line)

    with open(log_file, "a", encoding="utf-8") as f:
        f.write(line + "\n")
