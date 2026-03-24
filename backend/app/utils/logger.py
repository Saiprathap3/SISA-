import logging
import json


class SimpleJsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "name": record.name,
            "message": record.getMessage(),
        }
        extras = {k: v for k, v in record.__dict__.items() if k not in ("name", "msg", "args", "levelname", "levelno", "pathname", "filename", "module", "exc_info", "exc_text", "stack_info", "lineno", "funcName", "created", "msecs", "relativeCreated", "thread", "threadName", "processName", "process")}
        if extras:
            payload.update(extras)
        return json.dumps(payload)


def get_logger(name: str) -> logging.Logger:
    """Return a structured JSON logger for the given name."""
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(SimpleJsonFormatter())
    logger.addHandler(handler)
    return logger


# Module-level logger for convenience across the app
logger = get_logger(__name__)

