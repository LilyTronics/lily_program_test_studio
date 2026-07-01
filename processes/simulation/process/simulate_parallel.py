"""
Test process for running a process parallel.
"""

from processes.base.process_base import ProcessBase
from processes.simulation.tasks.simulate_programming import TaskSimulateProgramming


class ProcessSimulateParallel(ProcessBase):

    name = "Process simulate parallel"
    n_serials_parallel = 2
    tasks = [TaskSimulateProgramming()]


if __name__ == "__main__":

    from processes.simulation.run_simulation_process import run_process

    run_process(ProcessSimulateParallel)
