"""
Manage the reports path.

Serial numbers:

<report_root>/
    |- serials/                                             # Store all serial specifc reports
    |   |- <serial number>/                                 # Reports for serial number
    |       |- run_<timestamp>/                             # Reports for the specific run
    |           |- <serial_number>_run_<timestamp>.html
    |           |- <serial_number>_run_<timestamp>.json
    |           |- <serial_number>_run_<timestamp>.log
    |
    |- work_orders/                                         # Store all work order specifc reports
        |- <work order ID>/                                 # Reports for work order
            |- run_<timestamp>/                             # Reports for the specific run
                |- <work order ID>_run_<timestamp>.html
                |- <work order ID>_run_<timestamp>.json
                |- <work order ID>_run_<timestamp>.log

timestamp: yyyymmdd_hhmmss

"""

import os

from src.models.os_specifics import sanitize_path
from src.models.time_converter import TimeConverter


def create_work_order_path(report_root, work_order, timestamp):
    return _create_path(timestamp, os.path.join(report_root, "work_orders"), work_order)

def create_serial_number_path(report_root, serial_number, timestamp):
    return _create_path(timestamp, os.path.join(report_root, "serials"), serial_number)

def _create_path(timestamp, report_root, item_id):
    timestamp = TimeConverter.get_time_string(timestamp, True)
    item_id = sanitize_path(item_id)
    path = os.path.join(report_root, item_id, f"run_{timestamp}")
    if not os.path.isdir(path):
        os.makedirs(path, exist_ok=True)
    return os.path.join(path, f"{item_id}_run_{timestamp}")


if __name__ == "__main__":

    from tests.unit_tests.model_tests.reports_path_test import ReportsPathTest

    ReportsPathTest().run()
