"""
Runs the process for a work order.
- Run the process for every serial number.
- Run sequential or parallel.
The process is run in a separate thread to make sure the GUI is not freezing.
"""

import threading

from src.models.process_registry import ProcessesRegistry


class ProcessRunner:

    _thread = None

    def __init__(self):
        raise Exception("This class should not be instantiated")

    ###########
    # Private #
    ###########

    @classmethod
    def _check_settings(cls, settings):
        if "work_order" not in settings or not settings["work_order"]:
            raise ValueError("The work order is not defined")
        if not isinstance(settings["work_order"], str):
            raise ValueError("The work order must be a string")
        if "process" not in settings or not settings["process"]:
            raise ValueError("The process is not defined")
        if not isinstance(settings["process"], str):
            raise ValueError("The process must be a string")
        if not ProcessesRegistry.get_process(settings["process"]):
            raise ValueError("The process does not exist")
        if "serial_numbers" not in settings or not settings["serial_numbers"]:
            raise ValueError("The serial numbers are not defined")
        if not isinstance(settings["serial_numbers"], list):
            raise ValueError("The serial numbers must be a list")
        if not all(isinstance(s, str) for s in settings["serial_numbers"]):
            raise ValueError("Not all the serial numbers are strings")
        if "output_folder" not in settings or not settings["output_folder"]:
            raise ValueError("The output folder is not defined")
        if not isinstance(settings["output_folder"], str):
            raise ValueError("The output folder must be a string")

    @classmethod
    def _process_thread(cls, settings):
        print(settings)

    ##########
    # Public #
    ##########

    @classmethod
    def run_process(cls, settings):
        if cls.is_running():
            raise Exception("A process is already running")
        cls._check_settings(settings)
        cls._thread = threading.Thread(target=cls._process_thread, args=(settings, ))
        cls._thread.daemon = True
        cls._thread.start()

    @classmethod
    def is_running(cls):
        return cls._thread is not None and cls._thread.is_alive()


if __name__ == "__main__":

    from tests.unit_tests.model_tests.process_runner_test import ProcessRunnerTest

    ProcessRunnerTest().run()
