"""
Base class for a process.
"""

import threading
import time

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

    def __init__(self, work_order):
        self.work_order = work_order

    ###########
    # Private #
    ###########

    def _run_tasks(self, serial, stop_event):
        for task in self.tasks:
            task.run(serial["serial_number"], serial["logger"])
            if stop_event.is_set():
                break

    ##########
    # Public #
    ##########

    @final
    def get_class_name(self):
        return self.__class__.__name__

    @final
    def run(self, serial_numbers, stop_event):
        threads = []
        for serial in serial_numbers:
            t = threading.Thread(target=self._run_tasks, args=(serial, stop_event), daemon=True)
            t.start()
            threads.append(t)

        while len([t for t in threads if t.is_alive()]) > 0:
            if stop_event.is_set():
                break
            time.sleep(0.1)


if __name__ == "__main__":

    from tests.unit_tests.processes_tests.process_base_test import ProcessBaseTest

    ProcessBaseTest().run()
