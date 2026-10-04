# Privacy notice — Publish a Plugin

Last updated October 4, 2026.

Publish a Plugin is a package of instructions, reference text, and two local scripts. It has no publisher-operated service, account, telemetry, or storage. The publisher does not receive or retain anything through this plugin.

## What the scripts do

`scripts/preflight.py` and `scripts/shrink_icon.py` import only the Python standard library: `argparse`, `json`, `os`, `re`, `struct`, `sys`, and `zlib`. They open no network connections, read no environment variables, start no subprocesses, and have no endpoint to send anything to.

`preflight.py` reads the plugin folder you name and prints findings. It writes nothing.

`shrink_icon.py` reads a PNG you name and rebuilds its compressed stream at maximum deflate. It decodes the result and compares it to the original, and refuses to write unless the pixels are identical. The one file it writes is the destination you specify.

## Why an automated scan will flag the reference files

This is worth stating plainly, because the finding is expected and the text that causes it is the point of the package.

`references/scanner-false-positives.md` documents the exact markdown patterns that make the directory's scanner report a credential read. To document them it has to contain them. The file holds the literal examples `$95M`, `$20/mo`, the bare token `env`, `printenv`, `export -p`, and the `${user_config.KEY}` remedy syntax. `SKILL.md` names `$PATH` and `$1` in the passage explaining which shell syntax must be preserved.

An automated scan reading prose as shell will read those as a plugin assembling a command at run time and reading the installer's environment. Neither is true. There is no code here that reads a credential, and the scripts above are the only executable parts.

Rewriting those examples would destroy the only reference that records this behaviour, which is the reason the package exists. They are left as published, and a reviewer confirming that is the expected outcome.

## What it reads and sends

It reads the plugin folder you point it at, on your machine. It sends nothing anywhere. There is no account to create and no data to retain.

For questions, use the [repository issue tracker](https://github.com/RachaelQuisel/publish-a-plugin/issues).
