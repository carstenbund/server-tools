"""NFS related helpers."""
from __future__ import absolute_import, print_function

import os

_EXPORTS = "/etc/exports"


def list_exports():
    """Return parsed NFS export entries."""
    exports = []
    if not os.path.exists(_EXPORTS):
        return exports
    fh = open(_EXPORTS, "r")
    try:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split()
            if parts:
                exports.append({"path": parts[0], "options": parts[1:]})
    finally:
        fh.close()
    return exports


def check_nfs_service():
    """Return True if rpc.nfsd process appears to be running."""
    proc_dir = "/proc"
    try:
        entries = os.listdir(proc_dir)
    except OSError:
        return False
    for name in entries:
        if not name.isdigit():
            continue
        cmdline = os.path.join(proc_dir, name, "cmdline")
        try:
            fh = open(cmdline, "rb")
            try:
                content = fh.read()
            finally:
                fh.close()
        except (IOError, OSError):
            continue
        if b"rpc.nfsd" in content:
            return True
    return False
