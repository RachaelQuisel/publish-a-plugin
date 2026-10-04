# When the scanner reads your markdown as shell

The directory scans every file, including documentation, for signs that a plugin reads credentials
and sends them somewhere. On a plugin made of markdown this produces false positives, because prose
*about* other products' settings looks like instructions *to* run them.

The finding reads roughly: *"Something in the plugin reads a credential (a token or API key) from
the user's environment or files and could send it to a server. A reviewer will check where it goes."*
It then names the files, and often pairs two findings into a two-step narrative; one file "reads the
environment", another "can send data off the machine".

## Patterns that trigger it

### A dollar sign in front of alphanumerics

Reported as *"a command assembled at run time"*. The scanner reads `$95M` the way a shell reads
`$95M`.

| Trips it | Write instead |
|---|---|
| `$95M` | `USD 95 million` |
| `$20/mo` | `USD 20/mo` |
| `$1,200` | `USD 1,200` |

### The bare token `env`, especially near a hostname and a credential word

Reported as *"is given the installer's environment (printenv / env / export -p / set)"*. A real
example that held a submission:

```
- **Setting:** API key hygiene
- **Recommend:** Env vars or a secret manager, never shared between teammates, rotate regularly.
```

That is advice about *another vendor's* console, in a file whose subject is that vendor's hostname.
The scanner read "env" + "key" + a remote host as a credential read beside a remote URL.

| Trips it | Write instead |
|---|---|
| `Env vars or a secret manager` | `Hold keys in a secret manager rather than in shell configuration` |
| `plain env vars` | `plain environment variables` |
| `` `.env` contents `` | `dotenv-file contents` |
| `printenv`, `export -p`, bare `set` | name the command only if the plugin genuinely runs it |

The phrase "environment variables" spelled out did not trigger it. The bare token `env` did.

## Patterns you should refuse to change

This matters as much as the fixes. Some `$` usages are **required syntax**, and rewriting them makes
your documentation wrong; a worse outcome than a review queue.

- **PowerShell**; `$true`, `$false`, `-AllowTranscription $false`. Keep them, inside code spans.
- **OData / query parameters**; `&$top=N`.
- **Claude Code's own command substitution**; `$ARGUMENTS` in `commands/*.md` is required for the
  command to work at all.

In practice these did not trigger findings when they sat inside backticks in files the scanner had
no other reason to flag. If one does get flagged, the honest answer is that it is correct syntax for
a third-party product, and that is exactly the kind of thing a reviewer confirms.

## How to decide

Ask one question: **does the plugin actually read a credential?**

If **no**; it is documentation, there is no code, no MCP server, no script. Reword the triggering
prose where rewording costs nothing, keep required syntax, and say so plainly in `PRIVACY.md`. If it
still holds, let a reviewer confirm it. That is a legitimate outcome, not a failure.

If **yes**; then the scanner is right and the `${user_config.KEY}` remedy is the correct one: ask
the user for the value through a config option marked sensitive, rather than reading it from their
machine.

**Never add a `user_config` option for a credential the plugin does not use.** It clears the finding
by making the manifest claim something untrue, and invites a question you then have to walk back.

## Sweep before you submit

`scripts/preflight.py` reports every one of these patterns with its file and line, and separates the
ones worth changing from the required syntax it knows to leave alone. Fixing them one file per
validation round is slow; the scanner reports the strongest finding, not all of them.
