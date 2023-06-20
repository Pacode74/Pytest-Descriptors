import logging
from descriptor_application_part_1.apps.exception_logging.exception_logging_warning_level import (
    function_that_logs_something_warning_level,
)
from descriptor_application_part_1.apps.exception_logging.exception_logging_info_level import (
    function_that_logs_something_info_level,
)
from descriptor_application_part_1.apps.exception_logging.logging_func import logger


# ---------------------------TestInGeneralExceptionLogging--------------------


def test_exception_logged_warning_level(caplog) -> None:
    """Testing exception was raised and logged at WARNING level"""
    function_that_logs_something_warning_level()
    assert "I am logging Modular Exception" in caplog.text


def test_exception_logged_info_level(caplog) -> None:
    """Testing exception was raised and logged at INFO level"""
    with caplog.at_level(logging.INFO):
        function_that_logs_something_info_level()
        print(f".caplog.text:{caplog.text}")
        assert "I am logging Modular Exception" in caplog.text


def test_logged_info_level(caplog) -> None:
    """Testing logging function at INFO level"""
    with caplog.at_level(logging.INFO):
        logger()  # imported from exception_logging
        print(f".caplog.text:{caplog.text}")
        assert "I am logging info level" in caplog.text
