import logging
from colorama import init, Fore
import sys
init(autoreset=True)


# Custom Formatter with Colors
class CustomFormatter(logging.Formatter):
    COLORS = {
        "DEBUG": Fore.CYAN,
        "INFO": Fore.GREEN,
        "WARNING": Fore.YELLOW,
        "ERROR": Fore.RED,
        "CRITICAL": Fore.RED + "\033[1m",  # Bold Red
    }

    def format(self, record):
        log_color = self.COLORS.get(record.levelname, "")
        default_format = "%(asctime)s - %(levelname)s - %(message)s"
        formatter = logging.Formatter(default_format)
        return log_color + formatter.format(record)


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()

console_handler.setFormatter(CustomFormatter())
# Remove any default handlers (fixes conflicts)
if logger.hasHandlers():
    logger.handlers.clear()

# Add the new handler
logger.addHandler(console_handler)
logger.propagate = False
# Test the logger
logger.debug("This is a DEBUG message.")
logger.info("This is an INFO message.")
logger.warning("This is a WARNING message.")
logger.error("This is an ERROR message.")
logger.critical("This is a CRITICAL message.")