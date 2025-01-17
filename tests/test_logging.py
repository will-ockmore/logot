from __future__ import annotations

import logging

from logot import Logot, logged

logger = logging.getLogger(__name__)


def test_capturing() -> None:
    with Logot().capturing() as logot:
        # Ensure log capturing is enabled.
        logger.info("foo bar")
        logot.assert_logged(logged.info("foo bar"))
    # Ensure log capturing is disabled.
    logger.info("foo bar")
    logot.assert_not_logged(logged.info("foo bar"))


def test_capturing_level_pass() -> None:
    with Logot().capturing(level=logging.INFO) as logot:
        logger.info("foo bar")
        logot.assert_logged(logged.info("foo bar"))


def test_capturing_level_fail() -> None:
    with Logot().capturing(level=logging.INFO) as logot:
        logger.debug("foo bar")
        logot.assert_not_logged(logged.debug("foo bar"))


def test_capturing_level_reset() -> None:
    assert logger.level == logging.NOTSET
    # Set a fairly non-verbose log level.
    try:
        with Logot().capturing(level=logging.INFO, name=__name__):
            # The logger will have been overridden for the required verbosity.
            assert logger.level == logging.INFO
        # When the capture ends, the logging verbosity is restored.
        assert logger.level == logging.NOTSET
    finally:
        # Whatever this test does, reset the logger to what it was!
        logger.setLevel(logging.NOTSET)


def test_capturing_name_exact_pass() -> None:
    with Logot().capturing(name=__name__) as logot:
        logger.info("foo bar")
        logot.assert_logged(logged.info("foo bar"))


def test_capturing_name_prefix_pass() -> None:
    with Logot().capturing(name="tests") as logot:
        logger.info("foo bar")
        logot.assert_logged(logged.info("foo bar"))


def test_capturing_name_fail() -> None:
    with Logot().capturing(name="boom") as logot:
        logger.info("foo bar")
        logot.assert_not_logged(logged.info("foo bar"))


def test_capture(logot: Logot) -> None:
    logger.info("foo bar")
    logot.assert_logged(logged.info("foo bar"))


def test_capture_levelno(logot: Logot) -> None:
    logger.log(logging.INFO, "foo bar")
    logot.assert_logged(logged.log(logging.INFO, "foo bar"))
