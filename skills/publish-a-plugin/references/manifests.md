# Manifests

## plugin.json

Everything the directory reads. `name` and `description` are the only strictly required fields for
the plugin to load; the rest are what make a listing look finished.

```json
{
  "name": "lowercase-kebab-case",
  "displayName": "Title Case Name",
  "description": "What it does for the reader, in one or two sentences.",
  "version": "1.0.0",
  "author": { "name": "Your Name" },
  "homepage": "https://github.com/<owner>/<repo>",
  "repository": "https://github.com/<owner>/<repo>",
  "license": "MIT",
  "keywords": ["five", "or", "six", "search", "terms"],
  "icon": "./icon.png",
  "documentationUrl": "https://github.com/<owner>/<repo>#readme",
  "supportUrl": "https://github.com/<owner>/<repo>/issues"
}
```

- **`name` must be lowercase kebab-case.** The directory requires it.
- **`displayName`** carries the human-readable listing name. Without it the directory shows the
  kebab-case name.
- **`icon`, `documentationUrl`, `supportUrl` belong here and nowhere else.** Putting them in
  `marketplace.json` does nothing.
- A `LICENSE` file **and** the `license` field. Compliance checks both.

## marketplace.json

```json
{
  "$schema": "https://anthropic.com/claude-code/marketplace.schema.json",
  "name": "marketplace-name",
  "description": "Short line shown for the marketplace itself.",
  "owner": { "name": "Your Name" },
  "plugins": [
    {
      "name": "same-as-plugin-json-name",
      "description": "Usually the same as plugin.json's description.",
      "source": "./",
      "category": "security",
      "homepage": "https://github.com/<owner>/<repo>"
    }
  ]
}
```

`source` is `"./"` for a root-layout plugin, or `"./plugins/<name>"` for the subdirectory layout.
The plugin entry's `name` must match `plugin.json`'s `name` exactly; `claude plugin tag` validates
that they agree.

## Version

Ship at `1.0.0`. The directory shows it, and `0.1.0` reads as unfinished to anyone browsing.

## Validation

```
claude plugin validate <path> --strict          # manifest
claude plugin validate <path>/skills --strict   # components
```

`--strict` only recognises `icon`, `documentationUrl` and `supportUrl` from **Claude Code 2.1.281**
onward. On an older build these fail and the manifest looks broken when the CLI is the problem.
Check with `claude --version` before debugging a manifest.

## Keeping files small

The directory reports total size and enforces a per-file limit; images are excluded from the 256 KiB
file cap but still count toward the total. Observed totals that passed: 737 KiB and 783 KiB, mostly
icon. A documentation-heavy plugin at 1.5 MB also passed.

If a single reference file approaches 256 KiB, split it **along seams that already exist** ;
section boundaries, a distinct appendix; rather than restructuring. Give each new file its own
header and a link back to the parent, and leave the parent pointing forward. A file at 90% of a cap
is a file that breaks the next time you add to it.
