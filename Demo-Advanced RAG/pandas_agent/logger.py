import logging
from logging.handlers import RotatingFileHandler
import sys

def setup_logging(log_file='log.log', level_str="DEBUG", use_console_handler=True, logger_name="document_ingestion"):
    """
    Sets up logging with file and optional console handlers.
    
    Parameters:
    -----------
    log_file : str
        The path to the log file. Default is 'log.log'.
    level_str : str
        Logging level as a string. Options: DEBUG, INFO, WARNING, ERROR, CRITICAL.
        Defaults to "DEBUG".
    use_console_handler : bool, optional
        If True, adds a console handler. Default is True.
    logger_name : str, optional
        The name of the logger to configure. Default is "root".
    
    Returns:
    --------
    logger : logging.Logger
        The configured logger instance.
    """
    # Validate and get logging level
    valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    if level_str.upper() not in valid_levels:
        print(f"Invalid log level: {level_str}. Defaulting to INFO.")
        level = logging.INFO
    else:
        level = getattr(logging, level_str.upper())

    # Get logger instance
    logger = logging.getLogger(logger_name)

    # Clear existing handlers if any
    if logger.hasHandlers():
        logger.handlers.clear()

    # Set logger level
    logger.setLevel(level)

    # Create file handler
    file_handler = RotatingFileHandler(log_file, maxBytes=30 * 1024 * 1024, backupCount=10)
    file_handler.setLevel(level)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    # Create console handler if enabled
    if use_console_handler:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

    # Ensure immediate log flushing
    for handler in logger.handlers:
        handler.flush = lambda: None  # Add flush attribute to each handler for safety

    return logger


def get_or_setup_logger(logger_name="ingestion", log_file='log.log', level_str="DEBUG", use_console_handler=True):
    """
    Return an existing logger if it has handlers, otherwise set it up.

    Parameters:
    -----------
    logger_name : str, optional
        The name of the logger to get or set up. Default is "root".

    log_file : str
        The path to the log file. Default is 'log.log'.

    level_str : str
        The logging level as a string. Valid options are:
        - "DEBUG"
        - "INFO"
        - "WARNING"
        - "ERROR"
        - "CRITICAL"
        Defaults to "DEBUG".

    use_console_handler : bool, optional
        If True, adds a console handler (StreamHandler).
        If False, no console handler will be added.
        Default is False.

    Returns:
    --------
    logger : logging.Logger
        The logger instance, either existing or newly configured.
    """
    logger = logging.getLogger(logger_name)

    # If the logger is already configured with handlers, return it
    if logger.handlers:
        return logger
    else:
        # Otherwise, set it up
        return setup_logging(log_file=log_file, level_str=level_str, use_console_handler=use_console_handler, logger_name=logger_name)
