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
