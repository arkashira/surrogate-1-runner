"""
A lightweight, streaming logger + metrics collector for pytest runs.

Usage:

    from logging_config import setup_logging, log_execution, ActionableErrorFormatter

    logger = setup_logging()
    with log_execution(logger):
        # run pytest or any other test harness