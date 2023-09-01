import logging

from core.enums import URSEnumClass

LOG_FORMAT_DEBUG = "%(levelname)s:%(message)s:%(pathname)s:%(funcName)s:%(lineno)d"


class LogLevels(URSEnumClass):
    """
    Log levels for the application
    """

    info = "INFO"
    warn = "WARN"
    error = "ERROR"
    debug = "DEBUG"


def configure_logging(LOG_LEVEL=LogLevels.error):
    """
    Configure logging for the application
    :param LOG_LEVEL: Log level to use
    :return: None
    """
    log_level = str(LOG_LEVEL).upper()  # cast to string
    log_levels = list(LogLevels)

    if log_level not in log_levels:
        # we use error as the default log level
        logging.basicConfig(level=LogLevels.error)
        return

    if log_level == LogLevels.debug:
        logging.basicConfig(level=log_level, format=LOG_FORMAT_DEBUG)
        return

    logging.basicConfig(level=log_level)
