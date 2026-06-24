"""
Unit test for the time converter.
"""

import time

from datetime import datetime

from src.models.time_converter import TimeConverter
from tests.lib.test_suite import TestSuite


class TimeConverterTest(TestSuite):

    def test_create_duration_time_string(self):
        test_values = [
            (    0, "00:00:00"),
            (   59, "00:00:59"),
            (   60, "00:01:00"),
            (   90, "00:01:30"),
            ( 3540, "00:59:00"),
            ( 3600, "01:00:00"),
            ( 3630, "01:00:30"),
            ( 5400, "01:30:00"),
            (82800, "23:00:00"),
            (86400, "1 days, 00:00:00"),
            (86430, "1 days, 00:00:30"),
            (86460, "1 days, 00:01:00"),
            (90000, "1 days, 01:00:00")
        ]
        for test_value in test_values:
            self.log.debug(f"Test value: {test_value[0]} seconds")
            value = TimeConverter.create_duration_time_string(test_value[0])
            self.log.debug(f"Result: {value}")
            self.fail_if(value != test_value[1],
                         f"Invalid value. Expected: {test_value[1]}")

    def test_get_time_string(self):
        timestamp = time.time()
        expected = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
        value = TimeConverter.get_time_string(timestamp)
        self.log.debug(f"Result: {value}")
        self.fail_if(value != expected, f"Invalid time string. Expected: {expected}")


if __name__ == "__main__":

    TimeConverterTest().run(True)
