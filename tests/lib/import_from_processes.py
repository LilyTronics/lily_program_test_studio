"""
Import from the processes package for testing.
"""

import os

from importlib.util import module_from_spec
from importlib.util import spec_from_file_location

import src.app_data as AppData


def import_class(filename, class_name):
    # We need to import using dynamic imports
    filename = os.path.join(AppData.PROCESSES_PATH, filename)
    name = os.path.basename(filename).split(".")[0]
    spec = spec_from_file_location(name, str(filename))
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, class_name)


if __name__ == "__main__":

    print(import_class(os.path.join("base", "process_base.py"), "ProcessBase"))
