"""Unified entry point for the steward server toolkit."""
from __future__ import absolute_import, print_function

import optparse
import sys

from steward.core import dispatcher, loader, remote_eval, reporter


def _convert_value(value):
    """Attempt to cast ``value`` to int or float when appropriate."""
    if value is None:
        return None
    # Booleans
    lowered = value.lower()
    if lowered in ("true", "false"):
        return lowered == "true"
    # Integer
    try:
        return int(value)
    except (TypeError, ValueError):
        pass
    # Float
    try:
        return float(value)
    except (TypeError, ValueError):
        pass
    return value


def _parse_pairs(items):
    """Return ``(args, kwargs)`` parsed from ``items``."""
    positional = []
    keyword = {}
    for item in items:
        if "=" in item:
            key, value = item.split("=", 1)
            keyword[key] = _convert_value(value)
        else:
            positional.append(_convert_value(item))
    return positional, keyword


def _config_to_dict(config):
    data = {}
    if hasattr(config, "sections"):
        for section in config.sections():
            items = {}
            for key, value in config.items(section):
                items[key] = value
            data[section] = items
    if hasattr(config, "defaults"):
        defaults = config.defaults()
        if defaults:
            data["DEFAULT"] = dict(defaults)
    return data


def _format_result(result, output):
    if output == "json":
        return reporter.to_json(result)
    return reporter.to_text(result)


def build_parser():
    parser = optparse.OptionParser(usage="%prog [options] <command> [<args>]")
    parser.add_option("--json", dest="json", action="store_true", default=False,
                      help="format output as JSON")
    parser.add_option("--config", dest="config_path", default=None,
                      help="path to configuration file")
    return parser


def handle_list(args):
    if not args:
        raise ValueError("list requires a target (tools/functions)")
    target = args[0]
    if target == "tools":
        return dispatcher.list_tools()
    if target == "functions":
        if len(args) < 2:
            raise ValueError("list functions requires a tool name")
        return dispatcher.list_functions(args[1])
    raise ValueError("unknown list target: %s" % target)


def handle_run(args):
    if len(args) < 2:
        raise ValueError("run requires <tool> <function> [args]")
    tool = args[0]
    function = args[1]
    positional, keyword = _parse_pairs(args[2:])
    return dispatcher.call(tool, function, *positional, **keyword)


def handle_config(config, args):
    if not args or args[0] != "show":
        raise ValueError("config requires the 'show' action")
    if len(args) == 1:
        return _config_to_dict(config)
    target = args[1]
    if "." in target:
        section, key = target.split(".", 1)
    else:
        section, key = target, None
    if key is None:
        if not config.has_section(section):
            raise ValueError("unknown config section: %s" % section)
        return dict(config.items(section))
    if config.has_option(section, key):
        return config.get(section, key)
    raise ValueError("unknown config option: %s.%s" % (section, key))


def handle_remote(config, args):
    if not args or args[0] != "eval":
        raise ValueError("remote requires the 'eval' action")
    payload = {}
    for item in args[1:]:
        if "=" not in item:
            continue
        key, value = item.split("=", 1)
        payload[key] = value
    url = None
    if config.has_option("general", "remote_eval_url"):
        url = config.get("general", "remote_eval_url")
    return remote_eval.evaluate(payload, url)


def main(argv=None):
    if argv is None:
        argv = sys.argv
    parser = build_parser()
    options, args = parser.parse_args(argv[1:])
    config = loader.load_config(options.config_path)
    if not args:
        parser.print_help()
        return 1
    command = args[0]
    rest = args[1:]
    try:
        if command == "list":
            result = handle_list(rest)
        elif command == "run":
            result = handle_run(rest)
        elif command == "config":
            result = handle_config(config, rest)
        elif command == "remote":
            result = handle_remote(config, rest)
        else:
            raise ValueError("unknown command: %s" % command)
    except Exception as exc:
        sys.stderr.write("error: %s\n" % exc)
        return 1
    output_format = "json" if options.json else "text"
    text = _format_result(result, output_format)
    sys.stdout.write(text + "\n")
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
