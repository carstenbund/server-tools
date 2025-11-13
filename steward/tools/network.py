"""Networking helpers."""
from __future__ import absolute_import, print_function

import os
import socket


def list_interfaces():
    """Return available network interfaces from /sys."""
    base = "/sys/class/net"
    try:
        names = os.listdir(base)
    except OSError:
        return []
    data = []
    for name in names:
        address_path = os.path.join(base, name, "address")
        try:
            fh = open(address_path, "r")
            try:
                mac = fh.read().strip()
            finally:
                fh.close()
        except (IOError, OSError):
            mac = ""
        data.append({"name": name, "mac": mac})
    return data


def resolve(hostname):
    """Resolve *hostname* to addresses."""
    if not hostname:
        return []
    try:
        info = socket.getaddrinfo(hostname, None)
    except socket.gaierror:
        return []
    results = []
    for family, socktype, proto, canon, sockaddr in info:
        entry = {
            "family": family,
            "type": socktype,
            "proto": proto,
            "address": sockaddr[0],
        }
        if canon:
            entry["canonical"] = canon
        results.append(entry)
    return results
