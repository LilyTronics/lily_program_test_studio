"""
OS Specifics.
"""

import os
import sys

from pathlib import Path

import src.app_data as AppData


def get_default_output_folder():
    return os.path.join(Path.home(), AppData.OUTPUT_FOLDER_NAME)

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


if __name__ =="__main__":

    print("Default output folder:", get_default_output_folder())
    print("User data dir:", get_user_data_dir())
