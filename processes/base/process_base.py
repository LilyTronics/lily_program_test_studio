"""
Base class for a process.
"""

from abc import ABC
from typing import final

from processes.base.task_base import TaskBase


class ProcessBase(ABC):

    name = ""
    n_serials_parallel = 1
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
        # Number of serials in parallel
        if not isinstance(cls.n_serials_parallel, int):
            raise ValueError(
                f"(Process) Number of serials parallel is not an integer in process {cls.__name__}"
            )
        # Number of serials in parallel
        if cls.n_serials_parallel < 1:
            raise ValueError(
                "(Process) Number of serials parallel is not greater or equal to 1 "
                f"in process {cls.__name__}"
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


    #################
    # Run the tasks #
    #################

    @final
    def run(self):
        for task in self.tasks:
            task.run()


if __name__ == "__main__":

    from tests.unit_tests.processes_tests.process_base_test import ProcessBaseTest

    ProcessBaseTest().run()
