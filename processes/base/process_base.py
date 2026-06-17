"""
Base class for a process.
"""

from abc import ABC


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
        if len(cls.tasks) == 0:
            raise ValueError(
                f"(Process) No tasks for process {cls.__name__}"
            )


if __name__ == "__main__":

    from tests.unit_tests.processes_tests.process_base_test import ProcessBaseTest

    ProcessBaseTest().run()
