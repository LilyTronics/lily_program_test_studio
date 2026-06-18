"""
Runs the test process.
"""

def run_process(process_class, work_order=None, serial_numbers=None):
    work_order = "TEST_ORDER" if work_order is None else work_order
    serial_numbers = ["SNR001", "SNR002", "SNR003"] if serial_numbers is None else serial_numbers

    proc = process_class(work_order, serial_numbers)
    proc.run()


if __name__ == "__main__":

    from processes.test_process.test_sequential import ProcessTestSequential

    run_process(ProcessTestSequential)
