"""Samba service helpers."""
from __future__ import absolute_import, print_function

import os
import subprocess

_CONFIG_PATHS = (
    "/etc/samba/smb.conf",
    "/usr/local/samba/lib/smb.conf",
)


def check_samba():
    """Return information about Samba configuration presence."""
    existing = []
    for path in _CONFIG_PATHS:
        if os.path.exists(path):
            existing.append(path)
    return {"configs": existing, "present": bool(existing)}


def list_shares():
    """Attempt to list configured shares using ``testparm`` if available."""
    cmd = ["testparm", "-s", "--parameter-name", "share"]
    try:
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except OSError:
        return {"command": cmd, "shares": []}
    stdout, _ = proc.communicate()
    output = stdout.decode("utf-8", "ignore")
    shares = []
    for line in output.splitlines():
        if line.strip() and not line.startswith("Load smb config"):  # coarse filter
            shares.append(line.strip())
    return {"command": cmd, "shares": shares}
