import logging
import sys

import sentry_sdk
from loguru import logger
from sentry_sdk import set_level, utils
from sentry_sdk.integrations.logging import BreadcrumbHandler, EventHandler, LoggingIntegration


def setup_loggers(config):
    logger.remove()
    logger.add(sys.stdout, colorize=True, level=config["logging"]["level"])

    if config["logging"].get("sentry"):
        sentry_env = "DEFAULT"
        if config["logging"]["sentry"].get("environment"):
            sentry_env = config["logging"]["sentry"]["environment"]
        logger.error(f"Sentry env: {sentry_env}")
        sentry_sdk.init(
            config["logging"].get("sentry", {}).get("dsn"),
            traces_sample_rate=0,
            max_breadcrumbs=100,
            debug=False,
            attach_stacktrace=True,
            include_local_variables=True,
            environment=sentry_env,
            max_value_length=1000,
        )

        # Sentry integration crunch
        set_level(config["logging"]["level"].lower())
        # utils.MAX_STRING_LENGTH = 1000

        _ = logger.add(
            BreadcrumbHandler(level=logging.DEBUG),
            level=logging.DEBUG,
        )

        _ = logger.add(
            EventHandler(level=logging.ERROR),
            level=logging.ERROR,
        )

        integrations = [
            LoggingIntegration(level=None, event_level=None),
        ]
        logger.debug("Sentry enabled")
