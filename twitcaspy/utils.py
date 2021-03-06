# Twitcaspy
# Copyright 2021 Alma-field
# See LICENSE for details.

from datetime import datetime

def fromtimestamp(unix_timestamp):
    if unix_timestamp is None:
        return None
    return datetime.fromtimestamp(unix_timestamp)
