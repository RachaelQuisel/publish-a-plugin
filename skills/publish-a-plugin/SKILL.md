---
name: publish-a-plugin
description: Build a Claude Code plugin that passes Anthropic's plugin directory submission on the first try, and work through the directory's validation findings when it doesn't. Use this whenever someone is creating, packaging, renaming, or submitting a Claude Code plugin, mentions claude.ai/directory/manage, pastes a validation report, hits a "policy hold", asks what to put in plugin.json or marketplace.json, asks how to answer the data-handling questions, or asks why their icon or a markdown file got flagged. Also use it before writing a new plugin at all, because several of the directory's constraints are much cheaper to design for than to retrofit.
---

# Publish a plugin

Getting a plugin into Anthropic's directory is two separate problems. Building a valid plugin is
easy and well documented. Getting through the directory's **security scanner** is the part that
surprises people, because it flags things that are not actually problems and the remedy it suggests
is sometimes wrong for your case.

This skill covers both, with the scanner behaviour written down because it is not documented
anywhere else.

## The order that avoids rework

1. Build the plugin and get `claude plugin validate <path> --strict` passing.
2. **Run `scripts/preflight.py` before you ever open the portal.** It checks the things the scanner
   flags — icon size, markdown patterns that read as shell variables, per-file size — and they are
   all cheaper to fix before a submission is in flight.
3. Push. Confirm the working tree is clean and in sync with origin.
4. Submit at `claude.ai/directory/manage` → **Submit new** → **Plugin bundle**.
5. Validate, fix, push, **Re-validate**.

## Five things that will cost you a cycle if you learn them late

**The portal scans one commit and does not refresh on its own.** A report is pinned to a SHA. After
any fix you push, you must press Re-validate. Conversely, if a submission is mid-flight and you push
an unrelated commit to the tracked branch, it gets picked up and rescanned. Finish one plugin before
touching its repo for another reason.

**Three warnings are unavoidable and you must not fix them.** Every plugin carrying the directory's
own listing fields gets flagged for them. Details in [references/validation-findings.md](references/validation-findings.md).
Removing the fields clears the warnings and breaks your listing.

**Icon size appears to matter more than icon content.** See [references/icons.md](references/icons.md).
`scripts/shrink_icon.py` fixes it losslessly.

**The scanner reads your markdown as if it were shell.** A dollar sign in front of a number, or the
bare word `env` near a hostname, can produce a finding that says your plugin reads credentials.
[references/scanner-false-positives.md](references/scanner-false-positives.md) has the patterns and,
importantly, which ones you should refuse to change.

**A policy hold is not a rejection.** The portal's own wording is that the plugin "stays held for
review" — a human looks at it. If your plugin genuinely has nothing to remove, leaving it and
letting a reviewer confirm is a legitimate outcome. Clearing the hold just skips the wait.

## Which reference to open

Read the one that matches the situation. Reading all six costs a lot of context and the answers do
not overlap.

| Situation | Open |
|---|---|
| A validation report with warnings or a hold | [validation-findings.md](references/validation-findings.md) |
| A credential or "command assembled at run time" finding | [scanner-false-positives.md](references/scanner-false-positives.md) |
| An icon that held, or any icon over ~750 KiB | [icons.md](references/icons.md) |
| Writing or fixing plugin.json / marketplace.json | [manifests.md](references/manifests.md) |
| Filling in the portal's five steps | [submission-walkthrough.md](references/submission-walkthrough.md) |
| Writing a privacy notice | [privacy-notice.md](references/privacy-notice.md) |

For most questions the body below plus one reference is enough.

## Repository layout

Two shapes work. The choice determines one field in the submission form, so decide deliberately.

**Plugin at the repository root** — simplest, and the plugin path field stays empty.

```
.claude-plugin/plugin.json
.claude-plugin/marketplace.json
skills/<skill-name>/SKILL.md
skills/<skill-name>/references/
skills/<skill-name>/examples/
commands/<command>.md          (optional)
icon.png
LICENSE
README.md
```

**Plugin in a subdirectory** — use when one repository holds several plugins. Enter `plugins/<name>`
in the submission form's plugin path field. The portal does appear to notice the layout on its own —
a real report showed the informational line *"marketplace.json lists 1 plugin folder in this
repository"* — but **whether a blank path validates has not been tested here**, so fill it in rather
than relying on detection.

```
.claude-plugin/marketplace.json          (repo root)
plugins/<name>/.claude-plugin/plugin.json
plugins/<name>/skills/<skill-name>/SKILL.md
plugins/<name>/icon.png
plugins/<name>/README.md
```

## Manifests

Full field reference in [references/manifests.md](references/manifests.md). The three that trip
people up:

- `name` must be **lowercase kebab-case**. The directory requires it. `displayName` carries the
  title-case name people read.
- `icon`, `documentationUrl` and `supportUrl` go in **`plugin.json` only, never `marketplace.json`**.
- `--strict` validation recognises those three fields from **Claude Code 2.1.281** onward; on an
  older build they fail and you will think your manifest is wrong when it is your CLI. *(Reported,
  not retested here — if `--strict` rejects these three fields, check `claude --version` before you
  touch the manifest.)*

## Writing the listing copy

The directory shows the plugin-folder `README.md` as the listing description, and `description` from
`plugin.json` as the short one. A shape that reads well:

- The name says the job.
- The first line states the before and after.
- Scannable bullets.
- One concrete number, because it signals the thing is real.
- A short close on how it works.

Each README should also say **what the plugin reads and what it sends**. The scanner looks for this,
and it is the single most useful paragraph you can write for a reviewer.

## Data handling answers

The portal asks four questions. For a plugin that is markdown and manifests with no backend, the
answers are below. The reasoning matters more than the answers, because a reviewer may ask:

| Question | Answer | Why |
|---|---|---|
| Reads or stores personal data? | **Reads only** | If it reads transcripts, profiles or settings pages, it reads names and emails. "No" would be false. It does not *store*, because there is no service — a user-initiated local save at a path they chose is the user storing their own file. |
| Sends data to a service other than declared connectors? | **No** | Fetching a public page is not sending user data to a service. |
| How long does your service retain data from Claude? | **Not retained** | There is no service. |
| Intended for users under 18? | **No** | Subject matter is not audience. A plugin that *discusses* children's data is not *for* children. |

**These answers describe one shape of plugin: markdown and manifests, no executable parts.** Check
before reusing them. If the plugin bundles an **MCP server, a hook, or a script**, three things
change at once:

- The credential finding in [scanner-false-positives.md](references/scanner-false-positives.md) may
  be **correct rather than a false positive**, and the `${user_config.KEY}` remedy becomes the right
  answer rather than the wrong one.
- "Sends data to a service" may be **Yes**, and it must then be listed in the README.
- Retention may no longer be "Not retained", because something you operate now receives data.

Answer from what the plugin does. A plugin with a backend that copies these answers is making a
false statement to a reviewer, which is a materially worse outcome than any warning.

## Optional but worth it

A **`PRIVACY.md`** in the plugin folder is not required — plugins pass without one. It is the
cheapest way to settle a data-handling question before it is asked, and it is nearly mandatory in
spirit if your plugin touches a browser, reads account pages, or has a subject matter where its
absence would look odd. Template in [references/privacy-notice.md](references/privacy-notice.md).

## Bundled scripts

- **`scripts/preflight.py <plugin-dir>`** — run before every submission. Reports icon size against
  the observed ceiling, markdown patterns that read as shell, oversized files, missing manifest
  fields, and layout problems. Exits non-zero if anything would likely hold.
- **`scripts/shrink_icon.py <icon.png>`** — losslessly recompresses a PNG by rebuilding its IDAT
  stream at maximum deflate. Pixels are bit-identical; it verifies this and refuses to write if not.

Both are plain Python with no dependencies beyond the standard library, because the machines this
runs on do not reliably have Pillow or ImageMagick.

`preflight.py` allows `$true`, `$false`, `$top`, `$ARGUMENTS` and `$schema` as required third-party
syntax and flags every other `$`-prefixed token. If it flags something that is genuinely correct
syntax for a documented product — a `$PATH` in a shell example, a positional `$1` — that is a true
positive for the scanner's heuristic and a false positive for your intent. Decide the same way you
would for any other finding: keep syntax that must stay, and expect that file to draw a reviewer.

## When preflight is clean and it still holds

That is not a contradiction; preflight checks the patterns observed so far, not the scanner's whole
rule set. Work it in this order:

1. **Read which file and field the finding names.** The directory is specific about this, and the
   named file is usually the whole story.
2. **Ask whether the thing it describes is actually true of your plugin.** If the plugin has no
   executable parts, a credential finding cannot be literally true, and your job is to find the
   prose that resembles one.
3. **Do not apply a remedy that makes a manifest claim something untrue** to clear a finding. That
   trades a warning for a misstatement.
4. **Write the disclosure instead.** A `PRIVACY.md` that says plainly what the package does and does
   not do answers the reviewer's actual question.
5. **Accept the review.** A hold is a queue, not a refusal.

## Verifying it actually installs

Validation checks how a plugin is built, not whether it works. Before submitting:

```
claude plugin marketplace add <owner>/<repo>
claude plugin install <name>@<marketplace>
claude plugin details <name>
```

`details` reports the component inventory and the projected token cost, which is worth seeing — an
always-on cost above a few hundred tokens means your description is doing too much work.

One thing that looks like a failure and is not: **the skill registry is fixed at session start**, so
a freshly installed plugin is not invocable until the next session. Test the skill by following its
`SKILL.md` directly rather than concluding the install broke.
