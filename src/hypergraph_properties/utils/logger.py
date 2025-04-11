__all__ = ["get_logger"]

import logging
import os
import sys
from typing import TextIO

LOGGER_NAME: str = "hypergraph-properties"
LOGGER_FORMAT = "[%(name)s] [%(levelname)s] %(message)s"


LOGGING_ENABLED = os.getenv("LOGGING_ENABLED", "true")[0].lower() in ("t", "1")


class Formatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        record.levelname = record.levelname.lower().ljust(len("warning"))
        formatter = logging.Formatter(LOGGER_FORMAT)
        return formatter.format(record)


class StdoutHandler(logging.StreamHandler):
    def __init__(self, level: int = logging.NOTSET) -> None:
        logging.Handler.__init__(self, level)

    @property
    def stream(self) -> TextIO:
        return sys.stdout


def get_logger() -> logging.Logger:
    return logging.getLogger(LOGGER_NAME)


def _set_up_logging() -> None:
    hg_logger = logging.getLogger(LOGGER_NAME)
    hg_logger.propagate = False

    handler = StdoutHandler()
    handler.setFormatter(Formatter())
    hg_logger.addHandler(handler)

    hg_logger.setLevel(logging.INFO if LOGGING_ENABLED else logging.CRITICAL)

_set_up_logging()
