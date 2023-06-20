import logging


def function_that_logs_something_info_level() -> None:
    """Function that raises a ValueError exception.
    It catches that exception. It logs a warning level"""
    logger = logging.getLogger("MODULAR_LOGS")  # initialize the logger
    try:
        raise ValueError("Modular Exception")
    except ValueError as e:
        logger.info(f"I am logging {str(e)}")
