"""
Unit test for the processes model.
"""

import os

import src.app_data as AppData

from src.models.process_registry import ProcessesRegistry
from tests.lib.test_suite import TestSuite


class ProcessesTest(TestSuite):

    expected_nr_of_processes = -1

    def setup(self):
        for item in os.listdir(AppData.PROCESSES_PATH):
            folder = os.path.join(AppData.PROCESSES_PATH, item)
            if os.path.isdir(folder):
                for current_folder, sub_folders, filenames in os.walk(folder):
                    sub_folders.sort()
                    if "__pycache__" in current_folder:
                        continue
                    for filename in filenames:
                        if filename == "__init__.py" or not filename.endswith(".py"):
                            continue
                        fullname = os.path.join(current_folder, filename)
                        self.expected_nr_of_processes += self.get_processes_count(fullname)
        self.log.debug(f"Expected number of processes: {self.expected_nr_of_processes}")

    def get_processes_count(self, filename):
        n_processes = 0
        with open(filename, "r", encoding="utf-8") as fp:
            for line in fp.readlines():
                if "if __name__ == \"__main__\":" in line:
                    break
                if line.startswith("class ") and "ProcessBase" in line:
                    n_processes += 1
        return n_processes

    def on_progress(self, count, message):
        self.log.debug(f"(Progress): {count} - {message}")

    def test_list_processes(self):
        ProcessesRegistry.load(self.on_progress)
        processes = ProcessesRegistry.get_processes()
        self.log.debug("Processes:")
        for d in processes:
            self.log.debug(f"{d}")
        self.fail_if(len(processes) != self.expected_nr_of_processes,
            f"The numbers of processes is not correct, expected: {self.expected_nr_of_processes}")

    def test_reload_processes(self):
        self.log.debug("Reload processes")
        ProcessesRegistry.load(self.on_progress)
        processes = ProcessesRegistry.get_processes()
        for d in processes:
            self.log.debug(f"{d}")

    def test_get_process(self):
        processes = ProcessesRegistry.get_processes()
        self.fail_if(len(processes) == 0, "Processes required for this test")
        for process in processes:
            self.log.debug(f"Get process for {process.name}")
            process_class = ProcessesRegistry.get_process(process.name)
            self.log.debug(f"Process class: {process_class}")
            self.fail_if(process_class is None, "No process found")


if __name__ == "__main__":

    ProcessesTest().run(True)
