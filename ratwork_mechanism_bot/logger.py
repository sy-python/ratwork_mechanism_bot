import logging
from logging import handlers
import sys


logger = logging.getLogger("ratwork_mechanism_bot")
logger.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

file_handler = handlers.TimedRotatingFileHandler(
    "logs/ratwork_mechanism_bot.log", when="midnight", backupCount=7
)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
