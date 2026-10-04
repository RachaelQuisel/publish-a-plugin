# Validation findings, and which ones to act on

<!-- preflight-allow: documents-scanner-patterns -->


Every finding observed on real submissions, what it means, and what to do. The short version: most
warnings are structural and expected. Act on the policy holds.

## The three warnings every plugin gets

These appear on any plugin that carries the directory's listing fields. **Do not fix them.**

### Unrecognized field in plugin.json; `documentationUrl`, `supportUrl`

> *"The plugin directory reads 'documentationUrl' for the listing; Claude Code itself ignores it at
> load time. No action needed."*

The plugin **loader** does not read these; the **directory** does. The portal says "No action
needed" itself, and notes that other listing-only fields such as `privacyPolicyUrl` are reported the
same way and are fine to keep.

### Field from another tool's manifest; `icon`

Same situation. The directory reads `icon` for the listing.

### Images and fonts passed without a code check

Informational, marked ⓘ rather than ⚠. The scanner is describing its own behaviour: it let a
well-formed image through without parsing it as code, and screened its printable text anyway. This
is not a finding about your file.

**Removing these three fields clears all three warnings and breaks your listing**; no docs link, no
support link, no icon. The warning is the cheaper outcome by a wide margin.

## Policy holds

A hold means a human reviews the plugin before it lists. It is not a rejection. Clearing it skips
the wait.

### Files or downloads the validator couldn't inspect

> *"Ship images and fonts without long embedded text (metadata, comments); otherwise leave them as
> they are and the plugin stays held for review."*

Check for embedded text first; most PNGs have none, in which case **the advice as written does not
apply to you**. Verify with `scripts/preflight.py`, which lists the PNG chunks. A clean PNG has only
`IHDR`, `IDAT` and `IEND`.

If it is clean, the remaining variable is size. See [icons.md](icons.md).

### Reads a credential and could send it off the machine

> *"Something in the plugin reads a credential (a token or API key) from the user's environment or
> files and could send it to a server."*

For a plugin that is markdown and manifests, this is a false positive, and the scanner names the
files that triggered it. Work through
[scanner-false-positives.md](scanner-false-positives.md) before changing anything.

**Do not take the `${user_config.KEY}` suggestion** unless a credential genuinely exists. Adding a
sensitive config option for a secret the plugin never uses makes the manifest *less* honest, and a
reviewer will ask what it is for.

The suggestion the portal offers that is usually right for documentation-only plugins: *"you can
leave it as it is and a reviewer confirms that."*

## Checks that pass silently

Worth knowing what is being measured so you can predict a hold:

- Repository fetched
- File count and total size, reported as e.g. "14 files, 783.9kB, within the size limits"
- `.claude-plugin/plugin.json` found and valid
- Skill, agent, command and hook inventory
- MCP servers, and whether they match what the directory expects
- Directory lints
- Name and publisher checks

A repo with a `marketplace.json` listing one plugin folder gets an informational note saying so.
That is expected for the subdirectory layout.
