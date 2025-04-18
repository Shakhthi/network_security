import os
from datetime import datetime

import logging

LOG_FILE = f"{datetime.now().strftime('%m-%d-%Y_%H-%M-%S')}.log"

logs_path = os.path.join(os.getcwd(), "logs", datetime.now().strftime('%m-%d-%Y'))

os.makedirs(logs_path, exist_ok=True)

LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)


""" if __name__ == "__main__":
    logging.info("Logger started")
    logging.info("Logger stopped") """
