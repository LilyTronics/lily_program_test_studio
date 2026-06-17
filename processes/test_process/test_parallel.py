"""
Test process for running a process parallel.
"""

from processes.base.process_base import ProcessBase
from processes.test_process.test_task import TaskTest


class ProcessTestParallel(ProcessBase):

    id = "1"
    name = "Process test parallel"
    tasks = [TaskTest()]
