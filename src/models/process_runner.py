"""
Runs the process for a work order.
- Run the process for every serial number.
- Run sequential or parallel.
The process is run in a separate thread to make sure the GUI is not freezing.
"""

import inspect
import threading
import time
import traceback

from src.models.console_redirect import ConsoleRedirect
from src.models.logger import Logger
from src.models.process_registry import ProcessesRegistry


class ProcessRunner:

    _thread = None
    _stop_event = threading.Event()
    _start_time = 0

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
        if settings.get("view_log_handler") is not None:
            log_methods = [("write", 1), ("flush", 0)]
            # Check if logger class instance has the correct methods
            for log_method in log_methods:
                attribute = getattr(settings["view_log_handler"], log_method[0], None)
                if not callable(attribute):
                    raise ValueError(
                        f"The view logger is missing callable method '{log_method[0]}'"
                    )
                sig = inspect.signature(attribute)
                params = sig.parameters
                if len(params) != log_method[1]:
                    raise ValueError(
                        f"Method {log_method[0]} for the view logger "
                        f"must have {log_method[1]} parameters"
                    )

    @classmethod
    def _create_logger(cls, view_handler):
        logger = Logger()
        ConsoleRedirect.add_logger(logger)
        if view_handler is not None:
            logger.add_handler(view_handler)
        return logger

    @classmethod
    def _process_thread(cls, settings):
        cls._start_time = int(time.time())
        try:
            proc_logger = cls._create_logger(settings.get("view_log_handler", None))
            process = ProcessesRegistry.get_process(settings["process"])(settings["work_order"])
            proc_logger.info(f"Run process: {process.name}")
            proc_logger.info(f"Total serial numbers: {len(settings["serial_numbers"])}")
            # Call run for a batch of serial numbers depending on process
            for i in range(0, len(settings["serial_numbers"]), process.n_serials_parallel):
                batch = [{
                    "serial_number": s,
                    "logger": cls._create_logger(settings.get("view_log_handler", None))
                    }
                    for s in settings["serial_numbers"][i:i + process.n_serials_parallel]
                ]
                process.run(batch, cls._stop_event)
                if cls._stop_event.is_set():
                    proc_logger.info("Process is aborted")
                    break

        except Exception:
            proc_logger.error(f"Exception when running process:\n{traceback.format_exc().strip()}")

    ##########
    # Public #
    ##########

    @classmethod
    def run_process(cls, settings):
        if cls.is_running():
            raise Exception("A process is already running")
        cls._check_settings(settings)
        cls._stop_event.clear()
        cls._thread = threading.Thread(target=cls._process_thread, args=(settings, ))
        cls._thread.daemon = True
        cls._thread.start()

    @classmethod
    def abort(cls):
        cls._stop_event.set()

    @classmethod
    def is_running(cls):
        return cls._thread is not None and cls._thread.is_alive()

    @classmethod
    def get_duration_time(cls):
        if cls._start_time > 0:
            return int(time.time()) - cls._start_time
        return 0


if __name__ == "__main__":

    from tests.unit_tests.model_tests.process_runner_test import ProcessRunnerTest

    ProcessRunnerTest().run()
