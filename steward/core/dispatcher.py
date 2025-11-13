"""Dispatcher for exposing tool functions via the CLI."""
from __future__ import absolute_import, print_function

import inspect

from steward.tools import TOOLS, ALLOWED_PREFIXES


def list_tools():
    """Return available tool names."""
    names = TOOLS.keys()
    try:
        return sorted(names)
    except TypeError:  # Python 2.6 keys is list
        return sorted(list(names))


def resolve_tool(name):
    """Return a module object for *name* or raise ``KeyError``."""
    if name not in TOOLS:
        raise KeyError(name)
    module_name = TOOLS[name]
    module = __import__(module_name, fromlist=["*"])
    return module


def list_functions(tool_name):
    """Return exposed functions for *tool_name*."""
    module = resolve_tool(tool_name)
    functions = []
    for attr in dir(module):
        if not attr.startswith(ALLOWED_PREFIXES):
            continue
        value = getattr(module, attr)
        if callable(value):
            doc = inspect.getdoc(value) or ""
            functions.append({"name": attr, "doc": doc})
    functions.sort(key=lambda item: item["name"])
    return functions


def call(tool_name, func_name, *args, **kwargs):
    """Invoke *func_name* from *tool_name* and return its result."""
    module = resolve_tool(tool_name)
    func = getattr(module, func_name, None)
    if func is None or not callable(func):
        raise AttributeError(func_name)
    return func(*args, **kwargs)
