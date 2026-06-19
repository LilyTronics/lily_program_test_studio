"""
Base class for a process.
"""

import inspect
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
        # Work order
        if not isinstance(work_order, str):
            raise ValueError(
                f"(Process) Work order is not a string for process {self.get_class_name()}"
            )
        self.work_order = work_order

    ###########
    # Private #
    ###########

    def _check_serial_numbers(self, serial_numbers):
        log_methods = ["info", "debug", "error"]

        if not isinstance(serial_numbers, list):
            raise ValueError(
                f"(Process) Serial Numbers is not a list for process {self.get_class_name()}"
            )
        if len(serial_numbers) == 0:
            raise ValueError(
                f"(Process) No serial numbers for process {self.get_class_name()}"
            )
        if len(serial_numbers) > self.n_serials_parallel:
            raise ValueError(
                f"(Process) Too many serial numbers for process {self.get_class_name()}"
            )
        if not all(isinstance(s, dict) for s in serial_numbers):
            raise ValueError(
                "(Process) Not all serial numbers are dictionaries for "
                f"process {self.get_class_name()}"
            )
        if not all("serial_number" in s for s in serial_numbers):
            raise ValueError(
                "(Process) Missing field serial_number for "
                f"process {self.get_class_name()}"
            )
        if not all("logger" in s for s in serial_numbers):
            raise ValueError(
                "(Process) Missing field logger for "
                f"process {self.get_class_name()}"
            )
        for serial in serial_numbers:
            # Check the serial number
            if not isinstance(serial["serial_number"], str):
                raise ValueError(
                    "(Process) Field serial_numer is not a string for "
                    f"process {self.get_class_name()}"
                )
            # Check if logger class instance has the correct methods
            for name in log_methods:
                method = getattr(serial["logger"], name, None)
                if not callable(method):
                    raise ValueError(
                        f"(Process) Field logger is missing callable method '{name}' for "
                        f"process {self.get_class_name()}"
                    )
                sig = inspect.signature(method)
                params = sig.parameters
                if len(params) != 1:
                    raise ValueError(
                        f"(Process) Method {name} for logger must have only one parameter for "
                        f"process {self.get_class_name()}"
                    )

    def _run_tasks(self, serial):
        for task in self.tasks:
            task.run(serial)

    ##########
    # Public #
    ##########

    @final
    def get_class_name(self):
        return self.__class__.__name__

    @final
    def run(self, serial_numbers):
        self._check_serial_numbers(serial_numbers)
        threads = []
        for serial in serial_numbers:
            t = threading.Thread(target=self._run_tasks, args=(serial,), daemon=True)
            t.start()
            threads.append(t)

        while len([t for t in threads if t.is_alive()]) > 0:
            time.sleep(0.1)


if __name__ == "__main__":

    from tests.unit_tests.processes_tests.process_base_test import ProcessBaseTest

    ProcessBaseTest().run()
