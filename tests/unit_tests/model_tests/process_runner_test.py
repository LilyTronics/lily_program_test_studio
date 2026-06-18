"""
Unit test for the processes runner.
"""

from src.models.process_runner import ProcessRunner
from src.models.work_order import WorkOrder
from tests.lib.test_suite import TestSuite
from tests.test_files.test_file import get_path


class ProcessRunnerTest(TestSuite):

    def test_run_sequential(self):
        WorkOrder.read_from_file(get_path("work_order_sequential.json"))
        ProcessRunner.run_process({
            "work_order": WorkOrder.get_work_order(),
            "process": WorkOrder.get_process(),
            "serial_numbers": WorkOrder.get_serial_numbers(),
            "output_folder": WorkOrder.get_output_folder()
        })



if __name__ == "__main__":

    ProcessRunnerTest().run(True)
