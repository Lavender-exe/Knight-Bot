import logging
from rich.logging import RichHandler
from config.__init__ import debug_path, session_path


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