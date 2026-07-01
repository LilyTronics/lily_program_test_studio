"""
Test process for running a process sequential.
"""

from processes.base.process_base import ProcessBase
from processes.simulation.tasks.simulate_programming import TaskSimulateProgramming


class ProcessSimulateSequential(ProcessBase):

    name = "Process simulate sequential"
    tasks = [TaskSimulateProgramming()]


if __name__ == "__main__":

    from processes.simulation.run_simulation_process import run_process

    run_process(ProcessSimulateSequential)
