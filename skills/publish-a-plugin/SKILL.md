---
name: publish-a-plugin
description: Interactively prepare a Claude Code plugin for directory review. Ask about the target, requested stage, and current finding. Check packaging, apply requested fixes, and explain observed scanner findings without promising approval.
---

# Publish a Plugin

Read [the conversation and writing rules](references/conversation-and-writing.md) before responding. Apply them to all user-facing text.

## Start the conversation

If the request has no details, ask:

1. "Which plugin folder or GitHub repository should I work with?"
2. "Do you want help preparing the package, fixing a validation finding, or submitting it?"
3. "What is the current problem? Paste the finding if you have one."

For a new plugin, ask what it does and who will use it before preparing the package. Keep a check limited to inspection. Apply fixes when requested. Push, submit, or change account settings only within the user's authorized request. If access or a required choice is missing, explain the gap and continue independent local work.


Getting a plugin into Anthropic's directory is two separate problems. Building a valid plugin is
easy and well documented. Getting through the directory's **security scanner** is the part that
surprises people, because it flags things that are not actually problems and the remedy it suggests
is sometimes wrong for your case.

This skill covers both, with the scanner behaviour written down because it is not documented
anywhere else.

## Check the package

1. Resolve the plugin folder and requested stage. Read the actual package before describing its behavior.
2. Run `claude plugin validate <path> --strict`.
3. Run `scripts/preflight.py <plugin-dir>`. It checks icon size, Markdown patterns, file sizes, manifest fields, and layout.
4. Read the focused reference for each finding. Confirm whether the finding describes actual code or quoted documentation.
5. Apply requested fixes. Preserve required product syntax, listing fields, licenses, and third-party attribution. Do not add a credential setting for a credential the plugin does not use.
6. Repeat the affected checks. State any unresolved result. A clean local check does not prove directory approval.

## Resolve directory findings

- A report applies to a specific commit. After a pushed fix, the portal must revalidate the new commit. A push to a tracked branch can trigger another scan.
- Observed listing-field warnings do not establish that `icon`, `documentationUrl`, or `supportUrl` should be removed. The directory uses these fields even when the loader ignores them.
- A policy hold means review is pending. It does not establish rejection or approval. Inspect the named file and explain a justified unchanged result when needed.
- A credential finding can refer to prose that resembles shell syntax. Check the executable parts before deciding it is a false finding. A package with a server, hook, or script needs a separate assessment.
- If the package actually needs a credential, use its supported sensitive configuration process. Preserve required syntax such as `${user_config.KEY}` when documenting it. Do not ask for a credential in chat.
- The icon size guidance comes from observed submissions. It is not a published size specification. The compression script verifies that decoded pixels are identical before writing.

## Choose a reference

| Situation | Reference |
| --- | --- |
| Validation warnings or a policy hold | [validation-findings.md](references/validation-findings.md) |
| Credential or command finding | [scanner-false-positives.md](references/scanner-false-positives.md) |
| Icon dimensions, size, or metadata | [icons.md](references/icons.md) |
| Manifest fields or layout | [manifests.md](references/manifests.md) |
| Submission source and account steps | [submission-walkthrough.md](references/submission-walkthrough.md) |
| Data-handling disclosure | [privacy-notice.md](references/privacy-notice.md) |

Read only the reference needed for the current issue. The observed findings may change. Check the current report before applying an older pattern.

## Package layout

A root plugin uses this layout:

```text
.claude-plugin/plugin.json
.claude-plugin/marketplace.json
skills/<skill-name>/SKILL.md
skills/<skill-name>/references/
icon.png
LICENSE
README.md
```

A repository containing several plugins keeps each package under `plugins/<name>`. Its root marketplace points to that package. For directory submission, enter the package path explicitly. Automatic path detection has not been confirmed for every layout.

The manifest name uses lowercase words separated by hyphens. `displayName` carries the readable title. Put `icon`, `documentationUrl`, and `supportUrl` in the plugin manifest, not the marketplace entry. Include the legal license file and its matching declaration. Preserve attribution for included material.

An older Claude Code version may reject listing fields that a newer version accepts. Check `claude --version` and the current error before removing a field.

## Write the listing

The directory uses the plugin README as its detailed description. Its manifest description supplies the short description.

- State the job and useful result.
- Describe confirmed capabilities in short bullets.
- Explain the opening questions and what happens after the answers.
- State what the plugin reads, writes, and sends.
- Explain required connections and material limitations.
- Use a number or time estimate only when a source supports it.

## Describe data handling

Answer from the package's actual instructions, tools, and executable parts. Do not copy another plugin's answers.

For an instruction-only package with no publisher-operated service, the user’s host still processes the supplied content. A review can read personal information from transcripts, profiles, or account pages. Disclose those reads and any tool requests.

A local file save, a request to a public website, a message to a connected service, and a publisher-operated backend have different effects. State which applies. A package with a server, hook, or script can have credential, network, or retention behavior that needs separate disclosure.

A privacy notice should name the data used, third-party requests, output locations, and host permission limits. Do not claim a technical guarantee enforced only by instructions.

## Push and submit when authorized

1. Confirm the requested fixes and local checks are complete.
2. Check the repository's current branch and local changes. Push only within the user's authorized scope. Do not overwrite another contributor's work.
3. For a requested directory submission, use the current portal at `claude.ai/directory/manage`. Resolve account access and missing choices before dependent actions.
4. Identify the repository, plugin path, and branch or tag. Validate that source.
5. Complete listing, data-handling, and compliance fields from the inspected package. Preserve exact claims the user has confirmed.
6. Submit when authorized. After a pushed fix, revalidate the new commit. Report the submitted state, findings, and any pending review.

If access is missing, explain what must be connected. Continue independent local preparation. Never report a saved draft as submitted or a submission as a visible listing.

## Installation checks

A manifest check confirms structure. It does not confirm the plugin can be installed. A repository
with `plugin.json` and no `marketplace.json` passes both `claude plugin validate --strict` and every
other preflight check, then fails on `marketplace add` with "Marketplace file not found". This
happens most often to a plugin moved out of a multi-plugin repository, because the marketplace
manifest stayed behind. `preflight.py` reports it, along with a `marketplace.json` whose entry name
does not match `plugin.json`, which breaks `install` the same way.

Test installation separately when it is requested or needed:

```text
claude plugin marketplace add <owner>/<repo>
claude plugin install <name>@<marketplace>
claude plugin details <name>
```

The skill registry is fixed at session start. A newly installed skill may require a new session. An isolated instruction test does not establish installation or behavior in another app.

## Bundled scripts

- `scripts/preflight.py` reads the target and reports findings. It does not write package files.
- `scripts/shrink_icon.py` recompresses a PNG with the Python standard library. It writes only after comparing the decoded image data.

The preflight check preserves known required syntax such as `$true`, `$false`, `$top`, `$ARGUMENTS`, and `$schema`. Other documented syntax such as `$PATH` and `$1` may produce a finding. Preserve required syntax and explain its purpose instead of making the example incorrect.
