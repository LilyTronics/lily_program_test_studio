"""
Unit test for the processes runner.
"""

from src.models.process_registry import ProcessesRegistry
from src.models.process_runner import ProcessRunner
from src.models.work_order import WorkOrder
from tests.lib.test_suite import TestSuite
from tests.test_files.test_file import get_path


class ProcessRunnerTest(TestSuite):

    _n_callbacks = 0

    def _start_batch_callback(self, serials):
        self.log.debug(f"Callback with serials: {serials}")
        self._n_callbacks += 1
        return True

    def setup(self):
        ProcessesRegistry.load()

    def test_run_exceptions(self):
        test_params = [
            ({}, "The work order is not defined"),
            ({"work_order": 1234}, "The work order must be a string"),
            ({"work_order": ""}, "The work order is not defined"),
            ({"work_order": "WO-TEST"}, "The process is not defined"),
            ({"process": 1234}, "The process must be a string"),
            ({"process": ""}, "The process is not defined"),
            ({"process": "not existing process"}, "The process does not exist"),
            ({"process": "Process simulate sequential"}, "The serial numbers are not defined"),
            ({"serial_numbers": "SNR001,SNR002"}, "The serial numbers must be a list"),
            ({"serial_numbers": []}, "The serial numbers are not defined"),
            ({"serial_numbers": ["SNR001", 2]}, "Not all the serial numbers are strings"),
            ({"serial_numbers": ["SNR001", "SNR002"]}, "The output folder is not defined"),
            ({"output_folder": 1234}, "The output folder must be a string"),
            ({"output_folder": ""}, "The output folder is not defined"),
        ]
        settings = {}
        for params in test_params:
            settings.update(params[0])
            try:
                self.log.debug(f"Test with settings: {settings}")
                ProcessRunner.run_process(settings)
                self.fail("No exception was raise while one was expected")
            except Exception as e:
                self.log.debug("Exception raised as expected")
                self.log.debug(f"Message: {e}")
                self.fail_if(str(e) != params[1], f"Wrong message, expected: '{params[1]}'")

    def test_run_process_sequential(self):
        self._n_callbacks = 0
        WorkOrder.read_from_file(get_path("work_order_sequential.json"))
        ProcessRunner.run_process({
            "work_order": WorkOrder.get_work_order(),
            "process": WorkOrder.get_process(),
            "serial_numbers": WorkOrder.get_serial_numbers(),
            "output_folder": WorkOrder.get_output_folder(),
            "test_logger": self.log,
            "start_batch_callback": self._start_batch_callback
        })
        self.wait_for(ProcessRunner.is_running, False, 60, 1)
        self.log.debug(f"Total callbacks: {self._n_callbacks}")
        self.fail_if(self._n_callbacks != 3, "Invalid number of callbacks, expected 3")

    def test_run_process_parallel(self):
        self._n_callbacks = 0
        WorkOrder.read_from_file(get_path("work_order_parallel.json"))
        ProcessRunner.run_process({
            "work_order": WorkOrder.get_work_order(),
            "process": WorkOrder.get_process(),
            "serial_numbers": WorkOrder.get_serial_numbers(),
            "output_folder": WorkOrder.get_output_folder(),
            "test_logger": self.log,
            "start_batch_callback": self._start_batch_callback
        })
        self.wait_for(ProcessRunner.is_running, False, 60, 1)
        self.log.debug(f"Total callbacks: {self._n_callbacks}")
        self.fail_if(self._n_callbacks != 2, "Invalid number of callbacks, expected 2")


if __name__ == "__main__":

    ProcessRunnerTest().run(True)
