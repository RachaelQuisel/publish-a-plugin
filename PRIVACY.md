# Privacy notice: Publish a Plugin

Last updated October 4, 2026.

Publish a Plugin is a package of instructions, reference text, and two local scripts. It has no publisher-operated service, account, telemetry, or storage. The publisher does not receive or retain anything through this plugin.

## What the scripts do

`scripts/preflight.py` and `scripts/shrink_icon.py` import only the Python standard library: `argparse`, `json`, `os`, `re`, `struct`, `sys`, and `zlib`. They open no network connections, read no environment variables, start no subprocesses, and have no endpoint to send anything to.

`preflight.py` reads the plugin folder you name and prints findings. It writes nothing.

`shrink_icon.py` reads a PNG you name and rebuilds its compressed stream at maximum deflate. It decodes the result and compares it to the original, and refuses to write unless the pixels are identical. The one file it writes is the destination you specify.

## Why an automated scan will flag the reference files

The reference intentionally includes the patterns discussed in observed findings.

`references/scanner-false-positives.md` documents the exact markdown patterns that make the directory's scanner report a credential read. To document them it has to contain them. The file holds the literal examples `$95M`, `$20/mo`, the bare token `env`, `printenv`, `export -p`, and the `${user_config.KEY}` remedy syntax. `SKILL.md` names `$PATH` and `$1` in the passage explaining which shell syntax must be preserved.

An automated scan may interpret the quoted prose as executable shell. The bundled scripts do not read credentials. There is no code here that reads a credential, and the scripts above are the only executable parts.

Preserve these literal examples so the reader can identify the reported patterns. A reviewer can inspect their documented purpose.

## What it reads and sends

The local scripts read the selected files and make no network requests. Requested GitHub or directory actions use the host’s available tools. Those services process requests under their own terms. The publisher operates no service for this package.

For questions, use the [repository issue tracker](https://github.com/RachaelQuisel/publish-a-plugin/issues).
