import logging
from datetime import datetime

def setup_logging():
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"{now}.log"

    file_handler = logging.FileHandler(log_filename)
    file_handler.setFormatter(logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    ))

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    ))

    logging.basicConfig(
        level=logging.INFO,
        handlers=[file_handler, console_handler]
    )