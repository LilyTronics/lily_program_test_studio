"""
Test for the process base class.
"""

import os
import threading

from tests.lib.import_from_processes import import_class
from tests.lib.test_suite import TestSuite


class ProcessBaseTest(TestSuite):

    WORK_ORDER = "TEST-ORDER"
    SERIALS = ["SNR001", "SNR002"]

    _process_base = None

    class TestLogger:
        def info(self): pass
        def debug(self): pass
        def error(self): pass


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
                self.log.debug(f"Test with params: {params[0]}")
                self._create_derived_class(params[0])
                self.fail("No exception was raise while one was expected")
            except Exception as e:
                self.log.debug("Exception raised as expected")
                self.log.debug(f"Message: {e}")
                self.fail_if(str(e) != params[1], f"Wrong message, expected: '{params[1]}'")

    def test_run_process_sequential(self):
        serials = [{"serial_number": s, "logger": self.log} for s in self.SERIALS]
        proc = import_class(os.path.join("simulation", "process", "simulate_sequential.py"),
                            "ProcessSimulateSequential")(self.WORK_ORDER)
        self.fail_if(proc.n_serials_parallel > 1, "Invalid number of serials parallel")
        proc.run(serials[0:proc.n_serials_parallel], threading.Event())

    def test_run_process_parallel(self):
        serials = [{"serial_number": s, "logger": self.log} for s in self.SERIALS]
        proc = import_class(os.path.join("simulation", "process", "simulate_parallel.py"),
                            "ProcessSimulateParallel")(self.WORK_ORDER)
        self.fail_if(proc.n_serials_parallel <= 1, "Invalid number of serials parallel")
        proc.run(serials[0:proc.n_serials_parallel], threading.Event())


if __name__ == "__main__":

    ProcessBaseTest().run()
