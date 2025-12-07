"""
Logger utility functions
"""
from .config import LoggerConfig


def get_logger(name=None):
    """
    Convenience function to get a configured logger

    Args:
        name: Logger name (if None, uses calling module name)

    Returns:
        Configured logger instance
    """
    if name is None:
        import inspect
        frame = inspect.currentframe().f_back
        name = frame.f_globals['__name__']

    return LoggerConfig.setup_logger(name)
