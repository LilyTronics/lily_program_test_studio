"""
Work order object.
"""

import json

import src.app_data as AppData


class WorkOrder():

    _data = {}

    _defaults = {
        "work_order": "",
        "process": "",
        "serial_numbers": [],
        "auto_start": False,
        "output_folder": AppData.OUTPUT_FOLDER
    }

    _test_fields = [
        ("work_order", str),
        ("process", str),
        ("serial_numbers", list, str),
        ("auto_start", bool),
        ("output_folder", str)
    ]

    ###########
    # Private #
    ###########

    @classmethod
    def _get_value(cls, key): return cls._data.get(key, cls._defaults[key])

    ##########
    # Public #
    ##########

    @classmethod
    def read_from_file(cls, filename):
        cls.clear()
        with open(filename, "r", encoding="utf-8") as fp:
            new_data = json.load(fp)
        # Validate data
        if not isinstance(new_data, dict):
            raise ValueError("Data is not a dictionary")
        for field in cls._test_fields:
            if field[0] in new_data:
                if not isinstance(new_data[field[0]], field[1]):
                    raise ValueError(f"The field '{field[0]}' must be type: '{field[1].__name__}'")
            if len(field) > 2:
                if not all(isinstance(x, field[2]) for x in new_data[field[0]]):
                    raise ValueError(f"The values in field '{field[0]}' "
                                     f"must be type: '{field[2].__name__}'")
        cls._data = new_data

    @classmethod
    def clear(cls): cls._data.clear()

    @classmethod
    def get_work_order(cls): return cls._get_value("work_order")

    @classmethod
    def get_process(cls): return cls._get_value("process")

    @classmethod
    def get_serial_numbers(cls): return cls._get_value("serial_numbers")

    @classmethod
    def get_auto_start(cls): return cls._get_value("auto_start")

    @classmethod
    def get_output_folder(cls): return cls._get_value("output_folder")


if __name__ == "__main__":

    from tests.unit_tests.model_tests.work_order_test import WorkOrderTest

    WorkOrderTest().run()
