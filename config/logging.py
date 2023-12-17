import logging
import os
from rich.logging import RichHandler

log_path = "config/logs"
debug_path = "config/logs/debug_logs.log"
session_path = "config/logs/session_logs.log"

if not os.path.exists(log_path):
    with open(log_path, 'w'): pass

if not os.path.exists(debug_path):
    with open(debug_path, 'w'): pass

if not os.path.exists(session_path):
    with open(session_path, 'w'): pass


logging.basicConfig(
    level="INFO", 
    format="%(message)s",
    datefmt="[%X]",
    handlers=[
        RichHandler(rich_tracebacks=True),
        logging.FileHandler(debug_path, mode='a', encoding="utf-8"),
        logging.FileHandler(session_path, mode='w', encoding="utf-8"),
    ],
)

log = logging.getLogger("rich")

def error(function):
    log.error(f"[red on grey]{function}[/red on grey]", extra={"markup": True})


def exception_error(function):
    log.exception(f"[red on grey]{function}[/red on grey]", extra={"markup": True})


def info(function):
    log.info(f"[cornflower_blue]{function}[/cornflower_blue]", extra={"markup": True})