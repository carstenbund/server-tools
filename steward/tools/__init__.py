"""Collection of high level server maintenance tools."""

TOOLS = {
    "users": "steward.tools.users",
    "samba": "steward.tools.samba",
    "nfs": "steward.tools.nfs",
    "fs": "steward.tools.fs",
    "proc": "steward.tools.processes",
    "logs": "steward.tools.logs",
    "net": "steward.tools.network",
    "sec": "steward.tools.security",
}

# prefixes we expose through the dispatcher
ALLOWED_PREFIXES = (
    "list_",
    "check_",
    "scan_",
    "get_",
    "show_",
    "find_",
    "free_",
    "load_",
)
