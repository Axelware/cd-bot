# Future
from __future__ import annotations

# Standard Library
import asyncio
import contextlib
import logging
import logging.handlers
import os
import sys
from collections.abc import Generator

# Packages
import setproctitle

# My stuff
from core import bot, config


RESET = "\u001b[0m"
BOLD = "\u001b[1m"
UNDERLINE = "\u001b[4m"
REVERSE = "\u001b[7m"
BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = (f"\u001b[{30 + i}m" for i in range(8))


@contextlib.contextmanager
def logger() -> Generator[None, None, None]:

    loggers: dict[str, logging.Logger] = {
        "bot":     logging.getLogger("bot"),
        "discord": logging.getLogger("discord"),
        "slate":   logging.getLogger("slate"),
    }

    for name, log in loggers.items():

        file_handler = logging.handlers.RotatingFileHandler(
            filename=f"logs/{name}.log",
            mode="w",
            backupCount=5,
            encoding="utf-8",
            maxBytes=2 ** 22
        )
        log.addHandler(file_handler)

        stream_handler = logging.StreamHandler()
        log.addHandler(stream_handler)

        if os.path.isfile(f"logs/{name}.log"):
            file_handler.doRollover()

        file_formatter = logging.Formatter(
            fmt="%(asctime)s "
                "[%(name) 30s] "
                "[%(filename) 20s] "
                "[%(levelname) 7s] "
                "%(message)s",
            datefmt="%I:%M:%S %p %d/%m/%Y"
        )
        file_handler.setFormatter(file_formatter)

        stream_formatter = logging.Formatter(
            fmt=f"{CYAN}%(asctime)s{RESET} "
                f"{YELLOW}[%(name) 30s]{RESET} "
                f"{GREEN}[%(filename) 20s]{RESET} "
                f"{BOLD}{REVERSE}{MAGENTA}[%(levelname) 7s]{RESET} "
                f"%(message)s",
            datefmt="%I:%M:%S %p %d/%m/%Y",
        )
        stream_handler.setFormatter(stream_formatter)

    loggers["bot"].setLevel(logging.DEBUG)
    loggers["discord"].setLevel(logging.INFO)
    loggers["slate"].setLevel(logging.INFO)

    try:
        yield
    finally:
        [log.handlers[0].close() for log in loggers.values()]


if __name__ == "__main__":

    os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
    os.environ["JISHAKU_HIDE"] = "True"
    os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True"

    setproctitle.setproctitle("CD-bot")

    try:
        # Packages
        import uvloop
        if sys.platform != "win32":
            asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    except ImportError:
        uvloop = None
    else:
        del uvloop

    with logger():
        cd = bot.CD()
        cd.run(config.TOKEN)
