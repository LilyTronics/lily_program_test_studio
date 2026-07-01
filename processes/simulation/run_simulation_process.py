"""
Runs the simulation processes.
"""

import threading


class TestLogger:
    def _print(self, m_type, message): print(f"{m_type:5} - {message}")
    def info(self, message): self._print("INFO", message)
    def debug(self, message): self._print("DEBUG", message)
    def error(self, message): self._print("ERROR", message)


def run_process(process_class, work_order=None, serial_numbers=None):
    work_order = "TEST_ORDER" if work_order is None else work_order
    serial_numbers = ["SNR001", "SNR002", "SNR003"] if serial_numbers is None else serial_numbers

    proc = process_class(work_order)
    for i in range(0, len(serial_numbers), proc.n_serials_parallel):
        serials = serial_numbers[i: (i + proc.n_serials_parallel)]
        print("Run process for serials:", serials)
        serials = [{"serial_number": s, "logger": TestLogger()} for s in serials]
        proc.run(serials, threading.Event())


if __name__ == "__main__":

    from processes.simulation.process.simulate_sequential import ProcessSimulateSequential

    run_process(ProcessSimulateSequential)
