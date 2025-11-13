"""Filesystem helpers."""
from __future__ import absolute_import, print_function

import os
import stat


def list_mounts():
    """Return mount entries from /proc/mounts when available."""
    path = "/proc/mounts"
    if not os.path.exists(path):
        return []
    data = []
    fh = open(path, "r")
    try:
        for line in fh:
            parts = line.split()
            if len(parts) >= 3:
                data.append({"device": parts[0], "mount": parts[1], "type": parts[2]})
    finally:
        fh.close()
    return data


def free_space(path):
    """Return free space information for *path* in bytes."""
    if not path:
        path = "/"
    try:
        stats = os.statvfs(path)
    except OSError:
        return {}
    return {
        "path": path,
        "total": stats.f_frsize * stats.f_blocks,
        "available": stats.f_frsize * stats.f_bavail,
        "used": stats.f_frsize * (stats.f_blocks - stats.f_bfree),
    }


def list_directory(path):
    """Return file metadata for items within *path* (non-recursive)."""
    if not path:
        path = "."
    entries = []
    try:
        names = os.listdir(path)
    except OSError:
        return entries
    for name in names:
        full = os.path.join(path, name)
        try:
            st = os.lstat(full)
        except OSError:
            continue
        entries.append(
            {
                "name": name,
                "path": full,
                "mode": stat.S_IMODE(st.st_mode),
                "size": st.st_size,
            }
        )
    return entries
