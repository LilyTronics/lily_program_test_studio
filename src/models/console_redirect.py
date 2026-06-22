"""
Redirects standard out and standard error to loggers.
"""

import sys


class ConsoleRedirect:

    TYPE_STDOUT = "stdout"
    TYPE_STDERR = "stderr"

    org_stdout = sys.stdout
    org_stderr = sys.stderr

    _loggers = {
        TYPE_STDOUT: [],
        TYPE_STDERR: []
    }

    def __init__(self):
        raise Exception("This class should not be instantiated")

    @classmethod
    def enable_redirect(cls):
        sys.stdout = _StdLogger(cls.TYPE_STDOUT)
        sys.stderr = _StdLogger(cls.TYPE_STDERR)

    @classmethod
    def restore_redirect(cls):
        sys.stdout = cls.org_stdout
        sys.stderr = cls.org_stderr

    @classmethod
    def add_logger(cls, logger):
        for _, loggers in cls._loggers.items():
            if logger not in loggers:
                loggers.append(logger)

    @classmethod
    def remove_logger(cls, logger):
        for _, loggers in cls._loggers.items():
            if logger in loggers:
                loggers.remove(logger)

    @classmethod
    def write(cls, std_type, message):
        for logger in cls._loggers[std_type]:
            getattr(logger, std_type)(message)


class _StdLogger:
    def __init__(self, std_type): self._type = std_type
    def write(self, message): ConsoleRedirect.write(self._type, message)
    def flush(self): pass


if __name__ == "__main__":

    import threading

    from src.models.logger import Logger

    def _generate_error():
        _ = 1 / 0

    ConsoleRedirect.enable_redirect()

    log = Logger()
    log.add_handler(open("temp/test.log", "w", encoding="utf-8"))
    log.add_handler(ConsoleRedirect.org_stdout)
    ConsoleRedirect.add_logger(log)
    print("Standard output message")

    # Generate error in thread to keep this code running
    t = threading.Thread(target=_generate_error, daemon=True)
    t.start()
    while t.is_alive(): pass

    ConsoleRedirect.restore_redirect()
