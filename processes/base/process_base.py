"""
Base class for a process.
"""

from abc import ABC

from processes.base.task_base import TaskBase


class ProcessBase(ABC):

    name = ""
    tasks = []

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        # Process name
        if cls.name is ProcessBase.name or not cls.name:
            raise ValueError(
                f"(Process) Process name is not set in process {cls.__name__}"
            )
        if not isinstance(cls.name, str):
            raise ValueError(
                f"(Process) Process name is not a string in process {cls.__name__}"
            )
        # Tasks
        if not isinstance(cls.tasks, list):
            raise ValueError(
                f"(Process) Tasks is not a list in process {cls.__name__}"
            )
        if len(cls.tasks) == 0:
            raise ValueError(
                f"(Process) No tasks for process {cls.__name__}"
            )
        if not all(isinstance(x, TaskBase) for x in cls.tasks):
            raise ValueError(
                f"(Process) Not all tasks are derived from TaskBase for process {cls.__name__}"
            )


if __name__ == "__main__":

    from tests.unit_tests.processes_tests.process_base_test import ProcessBaseTest

    ProcessBaseTest().run()
