import json
import logging
from typing import Optional


class CustomFormatter(logging.Formatter):
    """Custom formatter for logs with date, time, name, function, and message."""

    def __init__(self, format: str = 'text', datefmt: str = '%Y-%m-%d %H:%M:%S'):
        """
        Initialize the custom formatter.
        
        Args:
            format: Output format ('text' or 'json'). Defaults to 'text'.
            datefmt: Date format string. Defaults to '%Y-%m-%d %H:%M:%S'.
        """
        super().__init__(datefmt=datefmt)
        if format not in ('text', 'json'):
            raise ValueError(f"format must be 'text' or 'json', got '{format}'")
        self.output_format = format

    def format(self, record: logging.LogRecord) -> str:
        asctime = self.formatTime(record, self.datefmt)
        date, time = asctime.split(' ')
        name = record.name
        func_name = record.funcName
        message = record.getMessage()
        
        if self.output_format == 'json':
            log_data = {
                'date': date,
                'time': time,
                'name': name,
                'message': message
            }
            # Only include funcName if it's not '<module>'
            if func_name != '<module>':
                log_data['funcName'] = func_name
            return json.dumps(log_data)
        else:  # text format
            # Exclude funcName if it's '<module>'
            if func_name == '<module>':
                return f'{asctime} {name} {message}'
            else:
                return f'{asctime} {name} {func_name} {message}'


class CustomLogger:
    """Custom logger exposing date, time, class name, function name, and message."""

    def __init__(self, name: str, level: int = logging.INFO, format: str = 'text', handler: Optional[logging.Handler] = None):
        """
        Initialize the custom logger.
        
        Args:
            name: Logger name/identifier.
            level: Logging level. Defaults to logging.INFO.
            format: Output format ('text' or 'json'). Defaults to 'text'.
            handler: Optional logging handler. If not provided, StreamHandler is used.
        """
        self._name = name
        self._logger = logging.getLogger(name)
        self._logger.setLevel(level)
        self._logger.propagate = False

        # Clear existing handlers to allow format changes
        for existing_handler in self._logger.handlers[:]:
            self._logger.removeHandler(existing_handler)

        if handler is None:
            handler = logging.StreamHandler()
        handler.setFormatter(CustomFormatter(format=format))
        self._logger.addHandler(handler)

    def debug(self, message: str, *args, **kwargs) -> None:
        self._logger.debug(message, *args, stacklevel=2, **kwargs)

    def info(self, message: str, *args, **kwargs) -> None:
        self._logger.info(message, *args, stacklevel=2, **kwargs)

    def warning(self, message: str, *args, **kwargs) -> None:
        self._logger.warning(message, *args, stacklevel=2, **kwargs)

    def error(self, message: str, *args, **kwargs) -> None:
        self._logger.error(message, *args, stacklevel=2, **kwargs)

    def critical(self, message: str, *args, **kwargs) -> None:
        self._logger.critical(message, *args, stacklevel=2, **kwargs)

    def exception(self, message: str, *args, **kwargs) -> None:
        self._logger.exception(message, *args, stacklevel=2, **kwargs)

    @property
    def name(self) -> str:
        return self._name


def get_logger(name: str, level: int = logging.INFO, format: str = 'text', handler: Optional[logging.Handler] = None) -> CustomLogger:
    """Return a configured CustomLogger instance."""
    return CustomLogger(name=name, level=level, format=format, handler=handler)
