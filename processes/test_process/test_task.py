"""
Task for the test process
"""

import time

from processes.base.task_base import TaskBase


class TaskTest(TaskBase):

    name = "Test task"

    def run(self, serial_number, logger):
        logger.info(f"Run task: {self.name} for {serial_number}")
        logger.debug("Sleep several seconds")
        time.sleep(3)
        logger.debug("Done")


if __name__ == "__main__":

    from processes.common.test_run_process import run_process
    from processes.test_process.test_sequential import ProcessTestSequential

    run_process(ProcessTestSequential)
