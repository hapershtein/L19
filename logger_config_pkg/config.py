"""
Logging Configuration Module
Provides centralized logging setup with rotating file handlers
"""
import logging
import os
import time
from logging.handlers import RotatingFileHandler
from datetime import datetime


class LoggerConfig:
    """Centralized logging configuration with rotating file handlers"""

    _initialized = False

    @staticmethod
    def setup_logger(name, log_dir='Logs', max_bytes=10*1024*1024, backup_count=5):
        """
        Set up logger with rotating file handler and console output

        Args:
            name: Logger name (typically __name__ from calling module)
            log_dir: Directory for log files (default: 'Logs')
            max_bytes: Maximum size of each log file in bytes (default: 10MB)
            backup_count: Number of backup files to keep (default: 5)

        Returns:
            Configured logger instance
        """
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        logger = logging.getLogger(name)

        if logger.hasHandlers():
            return logger

        logger.setLevel(logging.DEBUG)

        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        console_formatter = logging.Formatter(
            '%(levelname)s - %(message)s'
        )

        log_filename = os.path.join(log_dir, f'{name}.log')
        file_handler = RotatingFileHandler(
            log_filename,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(file_formatter)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)
        console_handler.setFormatter(console_formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        return logger

    @staticmethod
    def setup_pipeline_logger(log_dir='Logs', max_bytes=10*1024*1024, backup_count=5):
        """
        Set up special pipeline logger that logs all agents to single file

        Args:
            log_dir: Directory for log files (default: 'Logs')
            max_bytes: Maximum size of each log file in bytes (default: 10MB)
            backup_count: Number of backup files to keep (default: 5)

        Returns:
            Configured logger instance
        """
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        logger = logging.getLogger('pipeline')

        if logger.hasHandlers():
            return logger

        logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            '%(asctime)s - [%(name)s] - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        log_filename = os.path.join(log_dir, 'pipeline_execution.log')
        file_handler = RotatingFileHandler(
            log_filename,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        return logger

    @staticmethod
    def get_session_id():
        """Generate a unique session ID for this execution"""
        return datetime.now().strftime('%Y%m%d_%H%M%S')

    @staticmethod
    def log_separator(logger, title=''):
        """Log a separator line for readability"""
        separator = '=' * 70
        if title:
            logger.info(separator)
            logger.info(f' {title} ')
            logger.info(separator)
        else:
            logger.info(separator)

    @staticmethod
    def log_exception(logger, exc, context=''):
        """
        Log an exception with full traceback

        Args:
            logger: Logger instance
            exc: Exception object
            context: Optional context string describing where error occurred
        """
        if context:
            logger.error(f"Exception in {context}: {type(exc).__name__}: {exc}")
        else:
            logger.error(f"Exception: {type(exc).__name__}: {exc}")
        logger.exception("Full traceback:")

    @staticmethod
    def cleanup_old_logs(log_dir='Logs', days_to_keep=30):
        """
        Clean up log files older than specified days

        Args:
            log_dir: Directory containing log files
            days_to_keep: Number of days to keep logs (default: 30)
        """
        if not os.path.exists(log_dir):
            return

        current_time = time.time()
        cutoff_time = current_time - (days_to_keep * 86400)

        removed_count = 0
        for filename in os.listdir(log_dir):
            filepath = os.path.join(log_dir, filename)
            if os.path.isfile(filepath):
                file_modified = os.path.getmtime(filepath)
                if file_modified < cutoff_time:
                    try:
                        os.remove(filepath)
                        removed_count += 1
                    except Exception:
                        pass

        return removed_count
