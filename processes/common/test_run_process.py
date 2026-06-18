"""
Runs the test process.
"""

def run_process(process_class):
    work_order = "TEST_ORDER"
    serial_numbers = ["SNR0001", "SNR002"]

    proc = process_class()
    proc.run()


if __name__ == "__main__":

    from processes.test_process.test_sequential import ProcessTestSequential

    run_process(ProcessTestSequential)
