# The portal, step by step

`claude.ai/directory/manage` → **Submit new** → **Plugin bundle**. One submission per plugin.

## Prerequisites

- Paid claude.ai plan.
- GitHub account connected to claude.ai **in the submitting organization**.
- Public repo, or the Claude GitHub App installed plus the source-upload prompt accepted. A private
  repo can be validated and submitted; it must be public before the listing goes live.

## 1. Source

| Field | What to enter |
|---|---|
| Repository | The full `https://github.com/<owner>/<repo>` URL, or `owner/repo` |
| Plugin path | Empty for a root-layout plugin. `plugins/<name>` for the subdirectory layout. |
| Branch or tag | Empty to follow the default branch. A tag pins to its commit until you change it. |

Fill the path in for a subdirectory-layout plugin rather than relying on auto-detection. The portal
does report the layout informationally; *"marketplace.json lists 1 plugin folder in this
repository"*; but whether a blank path validates has not been tested here.

Then **Validate**. Work the findings with
[validation-findings.md](validation-findings.md).

## 2. Listing details

Prefills from `plugin.json`. The directory shows the plugin-folder `README.md` as the long listing
description, so that file is the listing copy, not an afterthought.

## 3. Data handling

Four questions. For a plugin that is markdown and manifests with no backend:

1. Reads or stores personal data → **Reads only**
2. Sends data to a service other than declared connectors → **No**
3. Retention of data received from Claude → **Not retained**
4. Intended for users under 18 → **No**

The reasoning is in the main SKILL.md. Answer from what your plugin actually does; if it has a
backend, these answers are wrong for you.

## 4. Compliance

- MIT (or your chosen licence), as both a `LICENSE` file and the `license` field.
- Sole author, original work, nothing vendored.
- Vendor names used nominatively, no logos or implied endorsement.

## 5. Review and submit

## Push updates (optional)

The portal offers a webhook so new commits are picked up immediately: GitHub → repo **Settings** →
**Webhooks** → **Add webhook**, with the payload URL and secret the dialog supplies, content type
`application/json`, and **just the push event**.

The secret is shown once. If it ends up in a screenshot, delete the screenshot once the webhook is
saved, or use **Rotate secret** on the plugin's Settings tab, which invalidates the old one
immediately.

## Sequencing several plugins

Finish one before touching another's repo, and keep each plugin in its own repository where you can.
The portal tracks a branch, so any push to it rescans whatever submission is in flight.
