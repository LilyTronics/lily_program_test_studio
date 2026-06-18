"""
Runs the process for a work order.
- Run the process for every serial number.
- Run sequential or parallel.
"""



class ProcessRunner:

    def __init__(self):
        raise Exception("This class should not be instantiated")

    ###########
    # Private #
    ###########



    ##########
    # Public #
    ##########

    @classmethod
    def run_process(cls, settings):
        print(settings)



if __name__ == "__main__":

    from tests.unit_tests.model_tests.process_runner_test import ProcessRunnerTest

    ProcessRunnerTest().run()
