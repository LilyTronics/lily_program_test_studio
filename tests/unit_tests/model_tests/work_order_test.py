"""
Work order model test.
"""

import src.app_data as AppData

from src.models.work_order import WorkOrder
from tests.lib.test_suite import TestSuite
from tests.test_files.test_file import get_path


class WorkOrderTest(TestSuite):

    _DEFAULT_VALUES = [
        (WorkOrder.get_work_order, "", "test order"),
        (WorkOrder.get_process, "", "test process"),
        (WorkOrder.get_serial_numbers, [], ["01234567", "89ABCDEF"]),
        (WorkOrder.get_auto_start, False, True),
        (WorkOrder.get_output_folder, AppData.OUTPUT_FOLDER, "C:\\test\\path")
    ]

    _TEST_FILES = [
        ("/path/to/invalid/filename.json" ,
         "[Errno 2] No such file or directory: '/path/to/invalid/filename.json'"),
        (get_path("work_order_no_json.json"),
         "Expecting value: line 1 column 1 (char 0)"),
        (get_path("work_order_invalid.json"),
         "Expecting ':' delimiter: line 2 column 12 (char 13)"),
        (get_path("work_order_no_dict.json"),
         "Data is not a dictionary"),
        (get_path("work_order_invalid_work_order.json"),
         "The field 'work_order' must be type: 'str'"),
        (get_path("work_order_invalid_process.json"),
         "The field 'process' must be type: 'str'"),
        (get_path("work_order_invalid_serial_numbers_list.json"),
         "The field 'serial_numbers' must be type: 'list'"),
        (get_path("work_order_invalid_serial_numbers_str.json"),
         "The values in field 'serial_numbers' must be type: 'str'"),
        (get_path("work_order_invalid_auto_start.json"),
         "The field 'auto_start' must be type: 'bool'"),
        (get_path("work_order_invalid_output_folder.json"),
         "The field 'output_folder' must be type: 'str'")
    ]

    def test_default_values(self):
        WorkOrder.clear()
        for dv in self._DEFAULT_VALUES:
            value = dv[0]()
            self.log.debug(f"{dv[0].__name__}: '{value}'")
            self.fail_if(value != dv[1], f"Wrong default value, expected: {dv[1]}")

    def test_invalid_files(self):
        for tf in self._TEST_FILES:
            self.log.debug(f"Test with file: '{tf[0]}'")
            try:
                WorkOrder.read_from_file(tf[0])
                self.fail("No exception was raise while one was expected")
            except Exception as e:
                if str(e) == "No exception was raise while one was expected":
                    raise
                self.log.debug("Exception raised as expected")
                self.log.debug(f"Message: {e}")
                self.fail_if(str(e) != tf[1], f"Wrong message, expected: '{tf[1]}'")

    def test_load_file(self):
        WorkOrder.read_from_file(get_path("work_order_valid.json"))
        for dv in self._DEFAULT_VALUES:
            value = dv[0]()
            self.log.debug(f"{dv[0].__name__}: '{value}'")
            self.fail_if(value == dv[1], "Value is still the default value")
            self.fail_if(value != dv[2], f"Wrong value, expected: '{dv[2]}'")


if __name__ == "__main__":

    WorkOrderTest().run()
