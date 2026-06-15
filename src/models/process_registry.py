"""
Provide access to processes.
"""

import inspect
import os

from importlib.util import module_from_spec
from importlib.util import spec_from_file_location

import src.app_data as AppData


class ProcessesRegistry:

    _processes = []

    _EXCLUDE_FOLDERS = []
    _EXCLUDED_FILES = []

    def __init__(self):
        raise Exception("This class should not be instantiated")

    ###########
    # Private #
    ###########

    # Dummy callback in case the progress callback is None
    @staticmethod
    def _callback(*_):
        pass

    @classmethod
    def _add_process(cls, attribute):
        matches = [x for x in cls._processes if x.name == attribute.name]
        if len(matches) > 0:
            raise Exception(f"Duplicate process name: '{attribute.name}'")
        cls._processes.append(attribute)

    ##########
    # Public #
    ##########

    @classmethod
    def load(cls, progress_callback=None):
        if progress_callback is None:
            progress_callback = cls._callback
        del cls._processes[:]
        files = []
        progress_callback(-1, f"Load processes from: {AppData.PROCESSES_PATH}")
        for current_path, subfolders, filenames in os.walk(AppData.PROCESSES_PATH):
            if "__pycache__" in current_path:
                continue
            subfolders.sort()
            for filename in filenames:
                if (os.path.splitext(filename)[0] in cls._EXCLUDED_FILES or
                    filename.startswith("_") or filename.endswith("_base.py")):
                    continue
                full_path = os.path.join(current_path, filename)
                if filename.endswith(".py") or filename.endswith(".pyc"):
                    files.append(full_path)
        total = len(files)
        progress_callback(-1, f"Load {total} processes")
        i = 0
        exceptions = []
        for i, filename in enumerate(files):
            rel_path = filename[len(AppData.PROCESSES_PATH) + 1:]
            progress_callback(100 * i / total, f"Load process from: {rel_path} ({i + 1}/{total})")
            name = os.path.basename(filename).split(".")[0]
            try:
                spec = spec_from_file_location(name, str(filename))
                module = module_from_spec(spec)
                spec.loader.exec_module(module)
                for attribute_name in dir(module):
                    attribute = getattr(module, attribute_name)
                    if inspect.isclass(attribute):
                        classes = [x.__name__ for x in inspect.getmro(attribute)]
                        if "ProcessBase" in classes:
                            classes.remove("object")
                            classes.remove("ProcessBase")
                            if "ABC" in classes:
                                classes.remove("ABC")
                            if len(classes) > 0:
                                cls._add_process(attribute)
            except Exception as e:
                exceptions.append((rel_path, str(e)))
        progress_callback(100 * (i + 1) / total, f"Processes loaded ({i + 1}/{total})")
        if len(exceptions) > 0:
            message = "One or more processes are not loaded due to errors:"
            for path, error in exceptions:
                message += f"\n{path}: {error}"
            raise Exception(message)

    @classmethod
    def get_processes(cls):
        return cls._processes

    @classmethod
    def get_process_names(cls):
        return [p.name for p in cls._processes]

    @classmethod
    def get_process(cls, name):
        matches = [x for x in cls._processes if x.name == name]
        return None if len(matches) != 1 else matches[0]


if __name__ == "__main__":

    from tests.unit_tests.model_tests.processes_test import ProcessesTest

    ProcessesTest().run()
