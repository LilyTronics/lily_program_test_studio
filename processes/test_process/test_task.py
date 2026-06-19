"""
Task for the test process
"""

import time

from processes.base.task_base import TaskBase


class TaskTest(TaskBase):

    name = "Test task"

    def run(self, serial_number):
        print("run task:", self.__class__.__name__, "for serial:", serial_number)
        print("Sleep several seconds")
        time.sleep(3)
        print("Done")


if __name__ == "__main__":

    from processes.common.test_run_process import run_process
    from processes.test_process.test_sequential import ProcessTestSequential

    run_process(ProcessTestSequential)
