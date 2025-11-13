"""Configuration loading helpers."""
from __future__ import absolute_import, print_function

import os

try:  # Python 3
    import configparser
except ImportError:  # Python 2
    import ConfigParser as configparser  # type: ignore

if hasattr(configparser, "SafeConfigParser"):
    _Parser = configparser.SafeConfigParser
else:  # Python 3.2+
    _Parser = configparser.ConfigParser

_DEFAULT_CONF = os.path.join(os.path.dirname(__file__), "..", "config", "steward.conf")


def load_config(path=None):
    """Load configuration from *path* or the default config file."""
    if path is None:
        path = os.path.abspath(_DEFAULT_CONF)
    parser = _Parser()
    if hasattr(parser, "read"):
        parser.read(path)
    return parser
