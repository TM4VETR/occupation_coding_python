import logging
from logging.handlers import TimedRotatingFileHandler
import os
import sys

PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

LOGGER_NAME = os.path.basename(PROJECT_DIR)

LOGS_DIR = os.path.join(PROJECT_DIR, "logs")
os.makedirs(LOGS_DIR, exist_ok=True)

# Create global logger
logger = logging.getLogger(LOGGER_NAME)
logger.setLevel(logging.DEBUG) # Global default level

# Log format
formatter = logging.Formatter(
    fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Prevent duplicate handlers if already added
if not logger.handlers:
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Rolling file handler
    log_file = os.path.join(LOGS_DIR, LOGGER_NAME + ".log")

    file_handler = TimedRotatingFileHandler(
        filename=log_file,
        when="midnight",
        interval=1,
        backupCount=14,
        encoding="utf-8",
        utc=False
    )

    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
