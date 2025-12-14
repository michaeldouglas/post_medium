import logging
import sys

from library.logging_filter import RequestIdFilter
from library.json_formatter import JsonLogFormatter


def setup_logging():
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonLogFormatter())
    handler.addFilter(RequestIdFilter())

    root = logging.getLogger()
    root.setLevel(logging.INFO)

    root.handlers.clear()
    root.addHandler(handler)
