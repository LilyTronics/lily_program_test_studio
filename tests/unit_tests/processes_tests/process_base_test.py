"""
Test for the process base class.
"""

import os

from tests.lib.import_from_processes import import_class
from tests.lib.test_suite import TestSuite


class ProcessBaseTest(TestSuite):

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

    def test_run_process_sequential(self):
        proc = import_class(os.path.join("test_process", "test_sequential.py"),
                            "ProcessTestSequential")()
        proc.run()

    def test_run_process_parallel(self):
        proc = import_class(os.path.join("test_process", "test_parallel.py"),
                            "ProcessTestParallel")()
        proc.run()


if __name__ == "__main__":

    ProcessBaseTest().run()
