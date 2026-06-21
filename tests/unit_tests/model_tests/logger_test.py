"""
Unit test for the logger.
"""

import os

from src.models.logger import Logger
from tests.lib.test_suite import TestSuite


class LoggerTest(TestSuite):

    _TEST_MESSAGES = [
        ("info", "This is an info message"),
        ("debug", "This is a debug message"),
        ("error", "This is a error message"),
        ("empty", ),
        ("info", "This is a\nmulti line message")
    ]
    _FILENAME = "test_log.txt"
    _logger = None
    _file_handler = None

    def setup(self):
        self._logger = Logger()
        self._file_handler = open(self._FILENAME, "w", encoding="utf-8")
        self._logger.add_handler(self._file_handler)

    def teardown(self):
        if os.path.isfile(self._FILENAME):
            os.remove(self._FILENAME)

    def test_logger(self):
        for message in self._TEST_MESSAGES:
            if message[0] == "info":
                self._logger.info(message[1])
            elif message[0] == "debug":
                self._logger.debug(message[1])
            elif message[0] == "empty":
                self._logger.empty_line()
            elif message[0] == "error":
                self._logger.error(message[1])

        # Remove handler
        self._logger.remove_handler(self._file_handler)
        self._logger.info("This message should not be in the file")

        self._file_handler.close()

        with open(self._FILENAME, "r", encoding="utf-8") as fp:
            lines = list(map(lambda x: x.rstrip(), fp.readlines()))
        self.fail_if(len(lines) == 0, "The log file is empty")

        # Check messages that should be in the file
        for message in self._TEST_MESSAGES:
            n_found = 0
            if message[0] == "empty":
                message = "empy line"
                for line in lines:
                    if line == "":
                        n_found += 1
            else:
                # Split up multi line messages
                parts = message[1].split("\n")
                for part in parts:
                    for line in lines:
                        if line.endswith(f"| {part}") and f"| {message[0].upper():6} |" in line:
                            n_found += 1
            self.fail_if(n_found != len(parts), f"Message '{message}' not found in the log file")

        # Check messages that should not be in the file
        for line in line:
            self.fail_if("This message should not be in the file" in line ,
                         "A message is in the file that should not be in the file")


if __name__ == "__main__":

    LoggerTest().run(True)
