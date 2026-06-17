"""
Test for the process base class.
"""

import os

from importlib.util import module_from_spec
from importlib.util import spec_from_file_location

import src.app_data as AppData

from tests.lib.test_suite import TestSuite


class ProcessBaseTest(TestSuite):

    _process_base = None

    def _create_derived_class(self, params):
        _ProcessTestClass = type("ProcessTest", (self._process_base, ), params)

    def setup(self):
        filename = os.path.join(AppData.PROCESSES_PATH, "base", "process_base.py")
        name = os.path.basename(filename).split(".")[0]
        self.log.debug(f"Import file: {filename}")
        spec = spec_from_file_location(name, str(filename))
        module = module_from_spec(spec)
        spec.loader.exec_module(module)
        self.log.debug(f"Module loaded: {module}")
        self._process_base = getattr(module, "ProcessBase")

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


if __name__ == "__main__":

    ProcessBaseTest().run()
