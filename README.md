# Publish a Plugin

Get your plugin through Anthropic's directory review on the first try.

Building a valid plugin is the easy half and it is well documented. The half that costs people a week is the directory's security scanner, which flags things that are not problems and sometimes suggests a remedy that is wrong for your case. This skill writes that behaviour down, because it is not documented anywhere else.

- Explains the scanner findings that look alarming and are not, including the credential finding a markdown-only plugin can trigger just by discussing credentials
- Names the three validation warnings you must **not** fix, because removing those fields clears the warnings and breaks your listing
- Ships `preflight.py`, which checks icon size, shell-looking markdown, file sizes, and missing manifest fields before a submission is in flight
- Ships `shrink_icon.py`, which rebuilds a PNG's compressed stream losslessly when an icon is over the roughly 750 KiB ceiling
- Gives the four data-handling answers the portal asks for, with the reasoning a reviewer may ask you to defend

How it works: run `preflight.py` against your plugin folder, fix what it names, push, then submit. Six reference files cover validation findings, scanner false positives, icons, manifests, the portal walkthrough, and privacy notices. Read only the one that matches your situation.

## Install

```
/plugin marketplace add RachaelQuisel/publish-a-plugin
/plugin install publish-a-plugin
```

## What this plugin reads and sends

It reads the plugin folder you point it at. It sends nothing anywhere. There is no service behind it, no account, and no telemetry. `preflight.py` and `shrink_icon.py` are plain Python with no dependencies beyond the standard library, they run locally, and `shrink_icon.py` verifies that the decoded image is bit-identical before it writes.

## Honesty about what is known

The scanner behaviour here is observed from real submissions, not published specification. Where something is inferred rather than confirmed, the reference files say so. The icon ceiling is the clearest example: three icons from one render pipeline straddle it, which is suggestive rather than proven, and the file says exactly that.

## License

MIT. See [LICENSE](LICENSE).
