"""
Test for the process base class.
"""

import os

from tests.lib.import_from_processes import import_class
from tests.lib.test_suite import TestSuite


class ProcessBaseTest(TestSuite):

    WORK_ORDER = "TEST-ORDER"
    SERIALS = ["SNR001", "SNR002", "SNR003"]

    _process_base = None


    def _create_derived_class(self, params):
        _ = type("ProcessTest", (self._process_base, ), params)

    def setup(self):
        self._process_base = import_class(os.path.join("base", "process_base.py"), "ProcessBase")

    def test_create_derived_class(self):
        test_params = [
            (
                {},
                "(Process) Process name is not set in process ProcessTest"
            ),
            (
                {"name": ""},
                "(Process) Process name is not set in process ProcessTest"
            ),
            (
                {"name": 123},
                "(Process) Process name is not a string in process ProcessTest"
            ),
            (
                {"name": "Test process"},
                "(Process) No tasks for process ProcessTest"
            ),
            (
                {"name": "Test process", "n_serials_parallel": "1"},
                "(Process) Number of serials parallel is not an integer in process ProcessTest"
            ),
            (
                {"name": "Test process", "n_serials_parallel": 0},
                "(Process) Number of serials parallel is not greater or equal to 1 in "
                "process ProcessTest"
            ),
            (
                {"name": "Test process", "tasks" : 1234},
                "(Process) Tasks is not a list in process ProcessTest"
            ),
            (
                {"name": "Test process", "tasks" : []},
                "(Process) No tasks for process ProcessTest"
            ),
            (
                {"name": "Test process", "tasks" : ["1234"]},
                "(Process) Not all tasks are derived from TaskBase for process ProcessTest"
            )
        ]
        for params in test_params:
            try:
                self._create_derived_class(params[0])
                self.fail("No exception was raise while one was expected")
            except Exception as e:
                self.log.debug("Exception raised as expected")
                self.log.debug(f"Message: {e}")
                self.fail_if(str(e) != params[1], f"Wrong message, expected: '{params[1]}'")

    def test_create_process_instance(self):
        proc_class = import_class(os.path.join("test_process", "test_sequential.py"),
                                  "ProcessTestSequential")
        test_params = [
            (
                (),
                "ProcessBase.__init__() missing 2 required positional arguments: "
                "'work_order' and 'serial_numbers'"
            ),
            (
                (None, ),
                "ProcessBase.__init__() missing 1 required positional argument: 'serial_numbers'"
            ),
            (
                (1234, None),
                "(Process) Work order is not a string for process ProcessTestSequential"
            ),
            (
                ("TEST-ORDER", {"SNR001", "SNR002"}),
                "(Process) Sserial Numbers is not a list for process ProcessTestSequential"
            ),
            (
                ("TEST-ORDER", []),
                "(Process) No serial numbers for process ProcessTestSequential"
            ),
            (
                ("TEST-ORDER", ["SNR001", 2]),
                "(Process) Not all serial numbers are strings for process ProcessTestSequential"
            ),
        ]
        for params in test_params:
            try:
                _ = proc_class(*params[0])
                self.fail("No exception was raise while one was expected")
            except Exception as e:
                self.log.debug("Exception raised as expected")
                self.log.debug(f"Message: {e}")
                self.fail_if(str(e) != params[1], f"Wrong message, expected: '{params[1]}'")

    def test_run_process_sequential(self):
        proc = import_class(os.path.join("test_process", "test_sequential.py"),
                            "ProcessTestSequential")(self.WORK_ORDER, self.SERIALS)
        self.fail_if(proc.n_serials_parallel > 1, "Invalid number of serials parallel")
        proc.run()

    def test_run_process_parallel(self):
        proc = import_class(os.path.join("test_process", "test_parallel.py"),
                            "ProcessTestParallel")(self.WORK_ORDER, self.SERIALS)
        self.fail_if(proc.n_serials_parallel <= 1, "Invalid number of serials parallel")
        proc.run()


if __name__ == "__main__":

    ProcessBaseTest().run()
