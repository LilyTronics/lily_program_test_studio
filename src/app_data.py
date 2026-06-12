"""
Application data.
"""

import os
import sys

from src.models.os_specifics import get_user_dir
from src.models.os_specifics import get_user_data_dir


APP_NAME = "Lily Program and Test Studio\u2122"   # \u2122 is the trademark symbol
VERSION = "1.0"
EXE_NAME = "LilyProgTestStudio"
COMPANY = "LilyTronics"

# Application path depends on if run from script or from the executable
if EXE_NAME in sys.executable:
    APP_PATH = os.path.dirname(sys.executable)
    # We must add the application path for import instruments in the executable
    sys.path.insert(0, str(APP_PATH))
else:
    APP_PATH = os.path.dirname(os.path.dirname(__file__))

SETTINGS_FILE = os.path.join(get_user_data_dir(), EXE_NAME, f"{EXE_NAME}.json")
PROCESSES_PATH = os.path.join(APP_PATH, "processes")
OUTPUT_FOLDER = os.path.join(get_user_dir(), "lily_prog_test_studio")


if __name__ == "__main__":

    print(f"{APP_NAME} V{VERSION}")
    print("App path      :", APP_PATH)
    print("Settings file:", SETTINGS_FILE)
    print("Output folder:", OUTPUT_FOLDER)
    print("Processes path:", PROCESSES_PATH)
