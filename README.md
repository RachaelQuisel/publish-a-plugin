# Publish a Plugin

Prepare a Claude Code plugin for directory review. Check the package, investigate validation findings, and apply requested fixes.

Start with `/publish-a-plugin:publish-a-plugin`. The plugin asks for a missing target, requested stage, and current problem. It waits for answers and remembers them. A complete request starts the work immediately.

- Validates the manifest and runs a local package check.
- Explains observed scanner findings and their limits.
- Preserves required syntax and listing fields.
- Compresses large PNG files without changing decoded pixels.
- Helps prepare data-handling disclosures from what the package actually does.

Read [how it works](Publish-A-Plugin-HowItWorks-2026-10-03.md). The six focused references cover findings, scanner patterns, icons, manifests, submission steps, and privacy notices.

## Claude Marketplace submission

Submitted to the [Claude Marketplace partner waitlist](https://claude.com/marketplace-partners) on **October 5, 2026**, through XRAY Automation. Submission confirmation was received; Marketplace eligibility and listing have not yet been confirmed.

## Install

```text
claude plugin marketplace add RachaelQuisel/publish-a-plugin
claude plugin install publish-a-plugin@publish-a-plugin
```

## Data and permissions

The local scripts read the plugin folder or PNG you choose. `preflight.py` reports findings and writes nothing. `shrink_icon.py` writes the selected image only after checking that decoded pixels are identical. These scripts make no network requests and read no credentials.

The assistant can use available GitHub or browser tools for a requested push or submission. Those services process the requests under their own terms. Inspection alone does not authorize a push, submission, or account change. The package has no publisher-operated service or telemetry.

The documented scanner behavior comes from observed submissions. It is not a published specification. Local validation does not prove directory approval. See [the privacy notice](PRIVACY.md).

## License

MIT. See [LICENSE](LICENSE).
