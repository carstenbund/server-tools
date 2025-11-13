"""Security oriented helpers."""
from __future__ import absolute_import, print_function

import os
import hashlib

_PASSWD = "/etc/passwd"
_SHADOW = "/etc/shadow"
_SUDOERS = "/etc/sudoers"


def check_file_permissions(path):
    """Return stat information about *path* if it exists."""
    try:
        st = os.stat(path)
    except OSError:
        return {"path": path, "exists": False}
    return {
        "path": path,
        "exists": True,
        "mode": st.st_mode & 0o7777,
        "uid": st.st_uid,
        "gid": st.st_gid,
    }


def check_core_files():
    """Return permission summaries for core security files."""
    return {
        "passwd": check_file_permissions(_PASSWD),
        "shadow": check_file_permissions(_SHADOW),
        "sudoers": check_file_permissions(_SUDOERS),
    }


def file_checksum(path):
    """Return the MD5 checksum for *path*."""
    try:
        fh = open(path, "rb")
    except (IOError, OSError):
        return {"path": path, "checksum": None}
    try:
        digest = hashlib.md5()
        while True:
            chunk = fh.read(8192)
            if not chunk:
                break
            digest.update(chunk)
    finally:
        fh.close()
    return {"path": path, "checksum": digest.hexdigest()}
