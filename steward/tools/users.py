"""User management helpers that avoid mutating system state."""
from __future__ import absolute_import, print_function

import os

try:
    basestring
except NameError:  # pragma: no cover
    basestring = str

_PASSWD = "/etc/passwd"


def list_users():
    """Return a list of user account dictionaries."""
    users = []
    if not os.path.exists(_PASSWD):
        return users
    fh = open(_PASSWD, "r")
    try:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split(":")
            if len(parts) < 7:
                continue
            users.append(
                {
                    "name": parts[0],
                    "uid": parts[2],
                    "gid": parts[3],
                    "comment": parts[4],
                    "home": parts[5],
                    "shell": parts[6],
                }
            )
    finally:
        fh.close()
    return users


def find_user(name):
    """Return a user entry or ``None`` if it does not exist."""
    if not name:
        return None
    all_users = list_users()
    for entry in all_users:
        if entry.get("name") == name:
            return entry
    return None
