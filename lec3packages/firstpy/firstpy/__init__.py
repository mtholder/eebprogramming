#!/usr/bin/env python
"""Template for the __init__ file in a python package."""
__all__ = ['tests']

import logging, os

def _get_logging_level():
    """Checks the environmental variable FIRSTPY_LOGGING_LEVEL for the correct
    level of logging output (DEBUG produces a lot of output, INFO less output,
    WARNING only shows warning or error messages, and ERROR inhibits every bit
    of output except the error messages.

    You can change the value of DEFAULT_LOGGING_LEVEL if you prefer to control
    the logging level by modifying the code rather than using environmental
    variables.

    """
    DEFAULT_LOGGING_LEVEL = logging.INFO

    if 'FIRSTPY_LOGGING_LEVEL' in os.environ:
        if os.environ['FIRSTPY_LOGGING_LEVEL'].upper() == "NOTSET":
            level = logging.NOTSET
        elif os.environ['FIRSTPY_LOGGING_LEVEL'].upper() == "DEBUG":
            level = logging.DEBUG
        elif os.environ['FIRSTPY_LOGGING_LEVEL'].upper() == "INFO":
            level = logging.INFO
        elif os.environ['FIRSTPY_LOGGING_LEVEL'].upper() == "WARNING":
            level = logging.WARNING
        elif os.environ['FIRSTPY_LOGGING_LEVEL'].upper() == "ERROR":
            level = logging.ERROR
        elif os.environ['FIRSTPY_LOGGING_LEVEL'].upper() == "CRITICAL":
            level = logging.CRITICAL
        else:
            level = DEFAULT_LOGGING_LEVEL
    else:
        level = DEFAULT_LOGGING_LEVEL
    return level

def get_logger(name="firstpy"):
    """Returns a logger object with name set as given

    The logger's level will be configured by a call to _get_logging_level.

    The environmental variable FIRSTPY_LOGGING_FORMAT controls the standard
    formatting that is applied to each message.  By default a rich message
    is used.  This formatting prints the time stamp of the message, the filename
    and line number and the message's level before printing the messag itself.

    """
    logger = logging.getLogger(name)
    level = _get_logging_level()
    rich_formatter = logging.Formatter("[%(asctime)s] %(filename)s (%(lineno)d): %(levelname) 8s: %(message)s")
    simple_formatter = logging.Formatter("%(levelname) 8s: %(message)s")
    raw_formatter = logging.Formatter("%(message)s")
    DEFAULT_FORMATTER = rich_formatter
    logging_formatter = DEFAULT_FORMATTER
    if 'FIRSTPY_LOGGING_FORMAT' in os.environ:
        if os.environ['FIRSTPY_LOGGING_FORMAT'].upper() == "RICH":
            logging_formatter = rich_formatter
        elif os.environ['FIRSTPY_LOGGING_FORMAT'].upper() == "SIMPLE":
            logging_formatter = simple_formatter
        elif os.environ['FIRSTPY_LOGGING_FORMAT'].upper() == "NONE":
            logging_formatter = None

    if logging_formatter is not None:
        logging_formatter.datefmt='%H:%M:%S'
    logger.setLevel(level)
    ch = logging.StreamHandler()
    ch.setLevel(level)
    ch.setFormatter(logging_formatter)
    logger.addHandler(ch)
    return logger




def some_function(arg):
    return 1
