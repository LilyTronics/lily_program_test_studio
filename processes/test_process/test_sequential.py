"""
Test process for running a process sequential.
"""

from processes.base.process_base import ProcessBase
from processes.test_process.test_task import TaskTest


class ProcessTestSequential(ProcessBase):

    id = "2"
    name = "Process test sequential"
    tasks = [TaskTest()]


if __name__ == "__main__":

    from processes.test_process.run_test_process import run_process

    run_process(ProcessTestSequential)
