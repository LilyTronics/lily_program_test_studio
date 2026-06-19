"""
Base class for a task of a process.
"""

from abc import ABC
from abc import abstractmethod


class TaskBase(ABC):

    name = ""

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        # Process name
        if cls.name is TaskBase.name or not cls.name:
            raise ValueError(
                f"(Task) Task name is not set in task {cls.__name__}"
            )
        if not isinstance(cls.name, str):
            raise ValueError(
                f"(Task) Task name is not a string in task {cls.__name__}"
            )

    @abstractmethod
    def run(self, serial_number):
        pass


if __name__ == "__main__":

    from tests.unit_tests.processes_tests.task_base_test import TaskBaseTest

    TaskBaseTest().run()
