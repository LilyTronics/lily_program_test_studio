"""
Handling test files
"""

import os


def _build_path(filename):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), filename))

def get_path(filename):
    return _build_path(filename)


if __name__ == "__main__":
    print(get_path("test_file.txt"))
