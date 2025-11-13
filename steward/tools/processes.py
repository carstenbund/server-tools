"""Process inspection helpers."""
from __future__ import absolute_import, print_function

import os


def list_processes():
    """Return a list of running process IDs with their command lines."""
    procs = []
    try:
        entries = os.listdir("/proc")
    except OSError:
        return procs
    for name in entries:
        if not name.isdigit():
            continue
        pid = name
        cmdline_path = os.path.join("/proc", pid, "cmdline")
        try:
            fh = open(cmdline_path, "rb")
            try:
                raw = fh.read().replace(b"\x00", b" ")
            finally:
                fh.close()
            cmd = raw.decode("utf-8", "ignore").strip()
        except (IOError, OSError):
            cmd = ""
        procs.append({"pid": pid, "command": cmd})
    return procs


def find_zombies():
    """Return processes that look like zombies."""
    zombies = []
    try:
        entries = os.listdir("/proc")
    except OSError:
        return zombies
    status_name = "status"
    for name in entries:
        if not name.isdigit():
            continue
        status_path = os.path.join("/proc", name, status_name)
        try:
            fh = open(status_path, "r")
        except (IOError, OSError):
            continue
        try:
            for line in fh:
                if line.startswith("State:") and "Z" in line:
                    zombies.append(name)
                    break
        finally:
            fh.close()
    return zombies


def load_average():
    """Return the system load averages."""
    try:
        fh = open("/proc/loadavg", "r")
    except (IOError, OSError):
        return {}
    try:
        data = fh.read().strip().split()
    finally:
        fh.close()
    if len(data) < 3:
        return {}
    return {"1min": data[0], "5min": data[1], "15min": data[2]}
