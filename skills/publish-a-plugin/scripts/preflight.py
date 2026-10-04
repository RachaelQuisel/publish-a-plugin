#!/usr/bin/env python3
"""Check a plugin against the directory's submission constraints before you open the portal.

Each validation round is slow and the scanner reports its strongest finding rather than all
of them, so fixing these one round at a time is the expensive way to do it.

    python3 preflight.py ~/Projects/personal/my-plugin

Exits non-zero if anything would likely hold. Standard library only.
"""
import argparse, json, os, re, struct, sys, zlib

ICON_CEILING = 768 * 1024      # observed, see references/icons.md
FILE_CAP = 256 * 1024          # per-file, images excluded
SIG = b'\x89PNG\r\n\x1a\n'
TEXT_CHUNKS = {b'tEXt', b'iTXt', b'zTXt', b'eXIf', b'iCCP'}

# $ followed by alphanumerics reads as a shell variable. These spellings are required
# syntax for third-party products and should be left alone.
ALLOWED_DOLLAR = re.compile(r'\$(true|false|top|ARGUMENTS|schema)\b', re.I)
DOLLAR = re.compile(r'\$[A-Za-z0-9_{][A-Za-z0-9_}]*')
ENV_TOKEN = re.compile(r'(?<![A-Za-z0-9_])(printenv|setenv|env)(?![A-Za-z0-9_])', re.I)
EXPORT_TOKEN = re.compile(r'\bexport -p\b')

problems, notes = [], []


def png_report(path):
    data = open(path, 'rb').read()
    if data[:8] != SIG:
        return None
    i, chunks = 8, []
    while i < len(data):
        (ln,) = struct.unpack('>I', data[i:i + 4])
        tag = data[i + 4:i + 8]
        chunks.append(tag)
        i += 12 + ln
        if tag == b'IEND':
            break
    (w, h) = struct.unpack('>II', data[16:24])
    meta = [t.decode('latin1') for t in chunks if t in TEXT_CHUNKS]
    return len(data), w, h, meta


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("plugin_dir")
    a = ap.parse_args()
    root = os.path.abspath(a.plugin_dir)

    # ---- manifest ----
    pj = None
    for cand in (os.path.join(root, ".claude-plugin", "plugin.json"),):
        if os.path.exists(cand):
            pj = cand
    if not pj:
        hits = []
        for dp, dn, fn in os.walk(root):
            if ".git" in dp:
                continue
            if "plugin.json" in fn and dp.endswith(".claude-plugin"):
                hits.append(os.path.join(dp, "plugin.json"))
        if len(hits) == 1:
            pj = hits[0]
            rel = os.path.relpath(os.path.dirname(os.path.dirname(pj)), root)
            notes.append(f"subdirectory layout: enter '{rel}' in the portal's Plugin path field")
        elif not hits:
            problems.append("no .claude-plugin/plugin.json found")
        else:
            notes.append(f"{len(hits)} plugin folders found; submit each separately")
            pj = hits[0]

    if pj:
        m = json.load(open(pj))
        print(f"plugin.json: {os.path.relpath(pj, root)}")
        name = m.get("name", "")
        if not re.fullmatch(r'[a-z0-9]+(-[a-z0-9]+)*', name or ""):
            problems.append(f"name '{name}' is not lowercase kebab-case; the directory requires it")
        for f in ("displayName", "description", "version", "author", "homepage",
                  "repository", "license", "icon", "documentationUrl", "supportUrl"):
            if not m.get(f):
                problems.append(f"plugin.json is missing '{f}'")
        if m.get("version", "").startswith("0."):
            notes.append(f"version {m['version']} reads as unfinished in a public listing")
        pdir = os.path.dirname(os.path.dirname(pj))
        if not os.path.exists(os.path.join(pdir, "LICENSE")) and \
           not os.path.exists(os.path.join(root, "LICENSE")):
            problems.append("no LICENSE file; compliance checks the file and the field")

        # listing fields must not be duplicated into marketplace.json
        mk = os.path.join(root, ".claude-plugin", "marketplace.json")
        if os.path.exists(mk):
            mm = json.load(open(mk))
            for entry in mm.get("plugins", []):
                for f in ("icon", "documentationUrl", "supportUrl"):
                    if f in entry:
                        problems.append(f"marketplace.json carries '{f}'; it belongs in plugin.json only")

        # ---- icon ----
        icon = os.path.join(pdir, (m.get("icon") or "./icon.png").lstrip("./"))
        if not os.path.exists(icon):
            problems.append(f"icon not found at {os.path.relpath(icon, root)}")
        else:
            size, w, h, meta = png_report(icon)
            print(f"icon: {os.path.relpath(icon, root)}  {w}x{h}  {size:,} bytes")
            if (w, h) != (1024, 1024):
                problems.append(f"icon is {w}x{h}; the directory expects 1024x1024")
            if size >= ICON_CEILING:
                problems.append(f"icon is {size:,} bytes, at or over the 768 KiB ceiling that "
                                f"correlates with a policy hold — run scripts/shrink_icon.py")
            if meta:
                problems.append(f"icon carries metadata chunks ({', '.join(meta)}) — "
                                f"shrink_icon.py drops them")

    # ---- markdown patterns ----
    flagged_dollar, flagged_env = [], []
    total = 0
    for dp, dn, fn in os.walk(root):
        dn[:] = [d for d in dn if d not in (".git", "node_modules")]
        for f in fn:
            p = os.path.join(dp, f)
            sz = os.path.getsize(p)
            total += sz
            if f.endswith(".md"):
                if sz > FILE_CAP:
                    problems.append(f"{os.path.relpath(p, root)} is {sz:,} bytes, over the "
                                    f"256 KiB per-file cap — split it along an existing seam")
                elif sz > FILE_CAP * 0.85:
                    notes.append(f"{os.path.relpath(p, root)} is {sz:,} bytes, within 15% of the "
                                 f"256 KiB cap; it breaks the next time you add to it")
                for n, line in enumerate(open(p, encoding="utf-8", errors="replace"), 1):
                    for mt in DOLLAR.finditer(line):
                        if not ALLOWED_DOLLAR.match(mt.group(0)):
                            flagged_dollar.append((os.path.relpath(p, root), n, mt.group(0)))
                    if ENV_TOKEN.search(line) or EXPORT_TOKEN.search(line):
                        flagged_env.append((os.path.relpath(p, root), n, line.strip()[:80]))

    print(f"total: {total:,} bytes")

    if flagged_dollar:
        problems.append(f"{len(flagged_dollar)} '$' pattern(s) that read as shell variables "
                        f"(\"a command assembled at run time\")")
        for f, n, tok in flagged_dollar[:12]:
            print(f"    {f}:{n}  {tok}")
    if flagged_env:
        problems.append(f"{len(flagged_env)} bare env/printenv/export token(s) "
                        f"(\"reads the installer's environment\")")
        for f, n, line in flagged_env[:12]:
            print(f"    {f}:{n}  {line}")

    print()
    for n in notes:
        print(f"note:    {n}")
    for p in problems:
        print(f"PROBLEM: {p}")
    if not problems:
        print("ready to submit")
    else:
        print(f"\n{len(problems)} problem(s). See references/scanner-false-positives.md before "
              f"changing anything — some '$' usages are required syntax and must stay.")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
