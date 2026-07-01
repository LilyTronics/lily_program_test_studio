"""
Task for the test process
"""

import time

from processes.base.task_base import TaskBase


class TaskSimulateProgramming(TaskBase):

    name = "Simulate programming"

    def run(self, serial_number, logger):
        logger.info(f"Run: {self.name} for {serial_number}")
        logger.debug("Connect to device")
        time.sleep(1)
        logger.debug("Erase device")
        time.sleep(1)
        logger.debug("Program device")
        time.sleep(3)
        logger.debug("Reboot device")
        time.sleep(2)
        logger.debug("Connect to device")
        time.sleep(1)
        logger.debug("Check if new firmware is running")
        logger.info("Programming device: pass")


if __name__ == "__main__":

    from processes.simulation.run_simulation_process import run_process
    from processes.simulation.process.simulate_sequential import ProcessSimulateSequential

    run_process(ProcessSimulateSequential)
