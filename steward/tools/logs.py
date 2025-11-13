"""Log scanning helpers."""
from __future__ import absolute_import, print_function

import os
import re

_DEFAULT_LOG = "/var/log/auth.log"
_FAIL_RE = re.compile(r"Failed password.*from (\S+)")


def scan_auth_log(path=None):
    """Return suspicious login attempts in *path*."""
    if not path:
        path = _DEFAULT_LOG
    if not os.path.exists(path):
        return []
    alerts = []
    fh = open(path, "r")
    try:
        for line in fh:
            match = _FAIL_RE.search(line)
            if match:
                alerts.append(match.group(1))
    finally:
        fh.close()
    return alerts


def tail(path, lines):
    """Return the last *lines* lines from *path*."""
    if not path or lines <= 0:
        return []
    if not os.path.exists(path):
        return []
    fh = open(path, "r")
    try:
        data = fh.readlines()
    finally:
        fh.close()
    return [line.rstrip("\n") for line in data[-lines:]]
