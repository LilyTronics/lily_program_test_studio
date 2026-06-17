"""
Test for the task base class.
"""

import os

from importlib.util import module_from_spec
from importlib.util import spec_from_file_location

import src.app_data as AppData

from tests.lib.test_suite import TestSuite


class TaskBaseTest(TestSuite):

    _task_base = None

    def _create_derived_class(self, params):
        _ProcessTestClass = type("TaskTest", (self._task_base, ), params)

    def setup(self):
        filename = os.path.join(AppData.PROCESSES_PATH, "base", "task_base.py")
        name = os.path.basename(filename).split(".")[0]
        self.log.debug(f"Import file: {filename}")
        spec = spec_from_file_location(name, str(filename))
        module = module_from_spec(spec)
        spec.loader.exec_module(module)
        self.log.debug(f"Module loaded: {module}")
        self._task_base = getattr(module, "TaskBase")

    def test_create_derived_class(self):
        test_params = [
            (
                {},
                "(Task) Task name is not set in task TaskTest"
            ),
            (
                {"name": ""},
                "(Task) Task name is not set in task TaskTest"
            ),
            (
                {"name": 123},
                "(Task) Task name is not a string in task TaskTest"
            ),
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

    TaskBaseTest().run()
