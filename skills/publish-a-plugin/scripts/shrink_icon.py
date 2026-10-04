#!/usr/bin/env python3
"""Losslessly shrink a PNG so it clears the plugin directory's inspection ceiling.

Rebuilds the compressed stream at maximum deflate without decoding pixels: the IDAT
chunks are concatenated, inflated to the filtered scanline data, and that same data is
deflated harder into a single chunk. The decoded image is bit-identical, which this
verifies before writing. Also drops any text/metadata chunks, which the directory's
hold message asks about.

Standard library only. The machines this runs on do not reliably have Pillow.

    python3 shrink_icon.py icon.png              # report only
    python3 shrink_icon.py icon.png --write      # replace in place
    python3 shrink_icon.py icon.png -o out.png   # write elsewhere
"""
import argparse, struct, sys, zlib

CEILING = 768 * 1024          # observed, not documented. See references/icons.md
TEXT_CHUNKS = {b'tEXt', b'iTXt', b'zTXt', b'eXIf', b'iCCP'}
SIG = b'\x89PNG\r\n\x1a\n'


def read_chunks(data):
    if data[:8] != SIG:
        raise ValueError("not a PNG")
    out, i = [], 8
    while i < len(data):
        (ln,) = struct.unpack('>I', data[i:i + 4])
        tag = data[i + 4:i + 8]
        out.append((tag, data[i + 8:i + 8 + ln]))
        i += 12 + ln
        if tag == b'IEND':
            break
    return out


def chunk(tag, payload):
    return (struct.pack('>I', len(payload)) + tag + payload
            + struct.pack('>I', zlib.crc32(tag + payload) & 0xffffffff))


def rebuild(data):
    chunks = read_chunks(data)
    ihdr = next(p for t, p in chunks if t == b'IHDR')
    idat = b''.join(p for t, p in chunks if t == b'IDAT')
    dropped = [t.decode('latin1') for t, _ in chunks if t in TEXT_CHUNKS]
    raw = zlib.decompress(idat)

    best = None
    for strategy in (zlib.Z_FILTERED, zlib.Z_DEFAULT_STRATEGY, zlib.Z_RLE):
        co = zlib.compressobj(9, zlib.DEFLATED, 15, 9, strategy)
        cand = co.compress(raw) + co.flush()
        if best is None or len(cand) < len(best):
            best = cand

    new = SIG + chunk(b'IHDR', ihdr) + chunk(b'IDAT', best) + chunk(b'IEND', b'')

    # prove the pixels survived: the filtered scanline stream must round-trip exactly
    check = zlib.decompress(b''.join(p for t, p in read_chunks(new) if t == b'IDAT'))
    if check != raw:
        raise RuntimeError("recompression changed the image data; refusing to write")
    return new, dropped, ihdr


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("png")
    ap.add_argument("-o", "--output")
    ap.add_argument("--write", action="store_true", help="replace the input file in place")
    a = ap.parse_args()

    data = open(a.png, 'rb').read()
    new, dropped, ihdr = rebuild(data)
    w, h, depth, color = struct.unpack('>IIBB', ihdr[:10])

    print(f"{a.png}")
    print(f"  {w}x{h}, bit depth {depth}, color type {color}")
    if (w, h) != (1024, 1024):
        print(f"  WARNING: the directory expects 1024x1024")
    print(f"  before {len(data):>9,} bytes   {'OVER' if len(data) >= CEILING else 'under'} the 768 KiB ceiling")
    print(f"  after  {len(new):>9,} bytes   {'OVER' if len(new) >= CEILING else 'under'} the 768 KiB ceiling"
          f"   ({100 * (len(data) - len(new)) / len(data):.1f}% smaller)")
    if dropped:
        print(f"  dropped metadata chunks: {', '.join(dropped)}")
    else:
        print("  no text or metadata chunks present")
    print("  pixels verified bit-identical")

    if len(new) >= CEILING:
        print("\n  Still over. Recompression is not enough — the next lever is the source render")
        print("  (fewer colours, less grain texture), not the encoding.")

    dest = a.output or (a.png if a.write else None)
    if dest:
        open(dest, 'wb').write(new)
        print(f"\n  wrote {dest}")
    else:
        print("\n  (report only; pass --write or -o to save)")
    return 0 if len(new) < CEILING else 1


if __name__ == "__main__":
    sys.exit(main())
