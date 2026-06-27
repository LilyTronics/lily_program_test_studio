"""
Unit test for the reports_path.
"""

import os
import shutil
import time

from src.models.reports_path import create_serial_number_path
from src.models.reports_path import create_work_order_path
from src.models.time_converter import TimeConverter
from tests.lib.test_suite import TestSuite


class ReportsPathTest(TestSuite):

    report_root = ""

    def setup(self):
        self.report_root = os.path.join(self.temp_folder, "test_reports")

    def teardown(self):
        shutil.rmtree(self.report_root, ignore_errors=True)

    def test_create_work_order_path(self):
        work_order = "WO-123456"
        timestamp_int = int(time.time())
        timestamp_str = TimeConverter.get_time_string(timestamp_int, True)
        expected_path = os.path.join(
            self.report_root, "work_orders", work_order, f"run_{timestamp_str}"
        )
        expected_file = os.path.join(expected_path, f"{work_order}_run_{timestamp_str}")
        result = create_work_order_path(self.report_root, work_order, timestamp_int)
        self.log.debug(f"Expected: {expected_file}")
        self.log.debug(f"Result  : {result}")
        self.fail_if(not os.path.isdir(expected_path), "The path was not created")
        self.fail_if(result != expected_file, "The filename is not as expected")

    def test_create_serial_path(self):
        serial_number = "SNR001"
        timestamp_int = int(time.time())
        timestamp_str = TimeConverter.get_time_string(timestamp_int, True)
        expected_path = os.path.join(
            self.report_root, "serials", serial_number, f"run_{timestamp_str}"
        )
        expected_file = os.path.join(expected_path, f"{serial_number}_run_{timestamp_str}")
        result = create_serial_number_path(self.report_root, serial_number, timestamp_int)
        self.log.debug(f"Expected: {expected_file}")
        self.log.debug(f"Result  : {result}")
        self.fail_if(not os.path.isdir(expected_path), "The path was not created")
        self.fail_if(result != expected_file, "The filename is not as expected")


if __name__ == "__main__":

    ReportsPathTest().run()
