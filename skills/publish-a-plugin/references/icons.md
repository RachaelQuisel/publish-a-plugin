# Icons

## Requirements

- **1024×1024 PNG.** RGBA is fine.
- Referenced as `"icon": "./icon.png"` in `plugin.json`, never in `marketplace.json`.
- Placed beside the `plugin.json` that references it. For the subdirectory layout that means
  `plugins/<name>/icon.png`, not the repository root.

## The size ceiling

**Observed, not documented.** Three icons from the same render pipeline, submitted the same week:

| Bytes | Result |
|---|---|
| 761,479 | passed |
| 793,042 | **policy hold** — "Files or downloads the validator couldn't inspect" |
| 816,698 | recompressed before submission, untested at original size |

Those straddle **768 KiB (786,432 bytes)**. That is two data points either side of a round number,
which is suggestive rather than proven. Treat 768 KiB as a ceiling to stay under; it costs nothing.

The hold's stated remedy — remove long embedded text — did not apply: all three PNGs contained only
`IHDR`, `IDAT` and `IEND`, with no `tEXt`, `iTXt`, `zTXt`, `eXIf` or `iCCP` chunk to remove.

## Getting under it without touching the image

`scripts/shrink_icon.py` rebuilds the PNG's compressed stream at maximum deflate. It does **not**
decode or re-encode pixels: it concatenates the `IDAT` chunks, inflates them to the filtered scanline
data, and deflates that same data harder into a single chunk. The decoded image is bit-identical, and
the script verifies this before writing.

Typical gain on a textured illustration is 7–8%, which was enough to clear the ceiling in every case
observed:

```
793,042 -> 729,153   (8.1% smaller)
816,698 -> 755,153   (7.5% smaller)
761,479 -> 702,929   (7.7% smaller)
```

If recompression is not enough, the next lever is the source render — fewer colours, less noise
texture — not the encoding. A flat-colour illustration at 1024² should not need 700 KB; these sizes
come from paper-grain texture, which compresses badly by design.

## Do not change an icon on a plugin mid-submission

The portal tracks the default branch and picks up new commits. If one plugin's submission has
already validated, pushing an icon fix for a *different* plugin to the *same* repo triggers a rescan
of the first. Separate repos avoid this entirely.
