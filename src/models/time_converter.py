"""
Module with time converter functions.
"""

import time

from datetime import datetime


class TimeConverter:

    _TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"
    _TIMESTAMP_FILE_FORMAT = "%Y%m%d_%H%M%S"

    @staticmethod
    def create_duration_time_string(seconds):
        d, h = divmod(seconds, 86400)
        m, s = divmod(h, 60)
        h, m = divmod(m, 60)
        output = ""
        if d > 0:
            output = f"{d} days, "
        output += f"{h:02}:{m:02}:{s:02}"
        return output

    @classmethod
    def get_time_string(cls, timestamp=time.time(), file_format = False):
        if file_format:
            return datetime.fromtimestamp(timestamp).strftime(cls._TIMESTAMP_FILE_FORMAT)
        return datetime.fromtimestamp(timestamp).strftime(cls._TIMESTAMP_FORMAT)
