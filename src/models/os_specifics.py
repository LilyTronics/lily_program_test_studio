"""
OS Specifics.
"""

import os
import sys
import re

from pathlib import Path


def get_user_dir():
    return Path.home()

def get_user_data_dir():
    extend_path = []
    match sys.platform:
        case "win32":
            extend_path = ["AppData", "Roaming"]
        case "darwin":
            extend_path = ["Library", "Application Support"]
        case _:  # Linux and others
            extend_path = [".local", "share"]
    return os.path.join(Path.home(), *extend_path)

def sanitize_path(name):
    return re.sub(r'[<>:"/\\|?*]', '_', name)


if __name__ =="__main__":

    print("User dir     :", get_user_dir())
    print("User data dir:", get_user_data_dir())
    print("Folder name  :", sanitize_path(
        "my/name\\that<contains>invalid:characters?for*a\"folder|name"))
