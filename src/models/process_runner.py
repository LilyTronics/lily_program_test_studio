"""
Runs the process for a work order.
- Run the process for every serial number.
- Run sequential or parallel.
The process is run in a separate thread to make sure the GUI is not freezing.
"""

import threading


class ProcessRunner:

    _thread = None

    def __init__(self):
        raise Exception("This class should not be instantiated")

    ###########
    # Private #
    ###########

    @classmethod
    def _check_settings(cls, settings):
        pass

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
