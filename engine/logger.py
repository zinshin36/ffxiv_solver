import logging
import os
from datetime import datetime
from engine.runtime_paths import LOG_DIR

def setup_logger():
    os.makedirs(LOG_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    logfile = os.path.join(LOG_DIR, f"run_{timestamp}.log")

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(logfile, encoding="utf-8"),
            logging.StreamHandler()
        ]
    )

    logging.info("===================================")
    logging.info("Application Started")
    logging.info(f"Log file: {logfile}")
    return logfile
