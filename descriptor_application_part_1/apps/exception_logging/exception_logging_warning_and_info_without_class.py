import logging

logger = logging.getLogger("MODULAR_LOGS")


def function_that_logs_something() -> None:
    try:
        raise ValueError("Modular Exception")
    except ValueError as e:
        logger.warning(f"I am logging {str(e)}")
