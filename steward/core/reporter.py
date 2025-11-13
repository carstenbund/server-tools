"""Output formatting helpers."""
from __future__ import absolute_import, print_function

import pprint

try:
    import json
except ImportError:  # pragma: no cover
    json = None


def to_text(data):
    """Return a text representation for *data*."""
    printer = pprint.PrettyPrinter(indent=2)
    return printer.pformat(data)


def to_json(data):
    """Return JSON output for *data* if possible."""
    if json is None:
        return to_text(data)
    return json.dumps(data, indent=2, sort_keys=True)
