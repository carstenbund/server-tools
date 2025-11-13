# server-tools

Linux maintenance utility providing a unified `steward` CLI with modular tools for common server administration tasks.

## Usage

```bash
python steward.py list tools
python steward.py list functions fs
python steward.py run fs free_space path=/
python steward.py config show general.log_file
```

Use `--json` to output structured data and `--config` to supply an alternate configuration file.

## Available tools

The `steward` dispatcher exposes several read-only helpers grouped by domain. Use
`python steward.py list functions <tool>` to discover the callable methods for a
specific tool.

| Tool | Module | Purpose |
| ---- | ------ | ------- |
| `users` | `steward.tools.users` | Inspect local UNIX accounts by listing entries from `/etc/passwd` or finding a single user record. |
| `samba` | `steward.tools.samba` | Check whether Samba configuration files exist and enumerate configured shares using `testparm` when available. |
| `nfs` | `steward.tools.nfs` | Review NFS exports from `/etc/exports` and detect whether the `rpc.nfsd` service appears to be running. |
| `fs` | `steward.tools.fs` | Gather filesystem information such as mounted filesystems, directory contents, and free space for a given path. |
| `proc` | `steward.tools.processes` | Inspect the `/proc` tree to list processes, detect zombie processes, and obtain system load averages. |
| `logs` | `steward.tools.logs` | Scan authentication logs for failed login attempts or tail arbitrary log files. |
| `net` | `steward.tools.network` | Explore network interfaces discovered in `/sys/class/net` and resolve hostnames to IP addresses. |
| `sec` | `steward.tools.security` | Examine permissions on critical security files and compute file checksums for integrity verification. |
