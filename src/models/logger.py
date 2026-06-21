"""
Logs messages to the given handlers.
"""

from datetime import datetime


class Logger:

    TYPE_INFO = "INFO"
    TYPE_DEBUG = "DEBUG"
    TYPE_ERROR = "ERROR"
    TYPE_STDOUT = "STDOUT"
    TYPE_STDERR = "STDERR"
    TYPE_EMPTY = "EMPTY"

    _TIME_STAMP_FORMAT = "%Y-%m-%d %H:%M:%S.%f"
    _LOG_FORMAT = "{} | {:6} | {}\n"

    def __init__(self):
        self._hanlders = []
        self._output = ""\

    ###########
    # Private #
    ###########

    def _handle_message(self, message_type, message_text=""):
        if message_type == self.TYPE_EMPTY:
            messages = ["\n"]
        else:
            messages = []
            timestamp = datetime.now().strftime(self._TIME_STAMP_FORMAT)[:-3]
            self._output += message_text
            while "\n" in self._output:
                index = self._output.find("\n")
                message = self._output[:index]
                self._output = self._output[index + 1:]
                messages.append(self._LOG_FORMAT.format(timestamp, message_type, message))
        for handler in self._hanlders:
            for message in messages:
                handler.write(message)
            handler.flush()

    ##########
    # Public #
    ##########

    def add_handler(self, handler):
        if handler not in self._hanlders:
            self._hanlders.append(handler)

    def remove_handler(self, handler):
        if handler in self._hanlders:
            self._hanlders.remove(handler)

    def info(self, message):
        self._handle_message(self.TYPE_INFO, f"{message}\n")

    def debug(self, message):
        self._handle_message(self.TYPE_DEBUG, f"{message}\n")

    def error(self, message):
        self._handle_message(self.TYPE_ERROR, f"{message}\n")

    def stdout(self, message):
        self._handle_message(self.TYPE_STDOUT, f"{message}")

    def stderr(self, message):
        self._handle_message(self.TYPE_STDERR, f"{message}")

    def empty_line(self):
        self._handle_message(self.TYPE_EMPTY)


if __name__ == "__main__":

    from tests.unit_tests.model_tests.logger_test import LoggerTest

    LoggerTest().run()
