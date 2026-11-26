#!/usr/bin/env python3
"""news-image-20261126 entry program.

Copies the bundled front-page image (entry.png, built by the agent in this
session) to the output directory after validating it as a whole PNG.
Standard library only, no network, deterministic: both runs write the
same bytes.

If entry.png is missing or fails validation, writes a valid 1x1
transparent PNG instead so the run still produces a whole image.
"""
import os
import struct
import sys
import zlib

MAX_BYTES = 1_048_576
MAX_DIM = 1024

PNG_SIG = b"\x89PNG\r\n\x1a\n"


def _chunk(ctype, data):
    crc = zlib.crc32(ctype)
    crc = zlib.crc32(data, crc) & 0xFFFFFFFF
    return struct.pack(">I", len(data)) + ctype + data + struct.pack(">I", crc)


def fallback_png():
    """A valid 1x1 transparent RGBA PNG, built from scratch."""
    ihdr = struct.pack(">IIBBBBB", 1, 1, 8, 6, 0, 0, 0)
    raw = b"\x00" + b"\x00\x00\x00\x00"  # filter 0 + one transparent pixel
    idat = zlib.compress(raw)
    return (PNG_SIG + _chunk(b"IHDR", ihdr)
            + _chunk(b"IDAT", idat) + _chunk(b"IEND", b""))


def validate_png(data):
    """Return (True, '') or (False, reason) for a whole PNG image."""
    if len(data) > MAX_BYTES:
        return False, "file over 1 MiB"
    if len(data) < 8 or data[:8] != PNG_SIG:
        return False, "bad PNG signature"
    pos = 8
    first = True
    seen_idat = False
    seen_iend = False
    width = height = 0
    while pos < len(data):
        if pos + 8 > len(data):
            return False, "truncated chunk header"
        length = struct.unpack(">I", data[pos:pos + 4])[0]
        ctype = data[pos + 4:pos + 8]
        end = pos + 12 + length
        if end > len(data):
            return False, "truncated chunk body"
        body = data[pos + 8:pos + 8 + length]
        stored_crc = struct.unpack(">I", data[pos + 8 + length:end])[0]
        crc = zlib.crc32(ctype)
        crc = zlib.crc32(body, crc) & 0xFFFFFFFF
        if crc != stored_crc:
            return False, "bad CRC in chunk %r" % ctype.decode("latin-1")
        if first and ctype != b"IHDR":
            return False, "IHDR is not the first chunk"
        first = False
        if ctype == b"IHDR":
            if length != 13:
                return False, "bad IHDR length"
            width, height = struct.unpack(">II", body[:8])
            if width > MAX_DIM or height > MAX_DIM:
                return False, "dimensions over 1024x1024"
            if width == 0 or height == 0:
                return False, "zero dimension"
        elif ctype == b"IDAT":
            seen_idat = True
        elif ctype == b"IEND":
            seen_iend = True
            if end != len(data):
                return False, "trailing bytes after IEND"
            break
        pos = end
    if not seen_idat:
        return False, "no IDAT chunk"
    if not seen_iend:
        return False, "no IEND chunk"
    return True, ""


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    src = os.path.join(here, "entry.png")
    data = None
    try:
        with open(src, "rb") as fh:
            data = fh.read()
    except OSError:
        data = None
    if data is not None:
        ok, reason = validate_png(data)
        if not ok:
            sys.stderr.write("entry.png invalid (%s); using fallback\n" % reason)
            data = None
    if data is None:
        data = fallback_png()
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.png")
    with open(out_path, "wb") as fh:
        fh.write(data)
    print("wrote %s (%d bytes, sha256 %s)"
          % (out_path, len(data), __import__("hashlib").sha256(data).hexdigest()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
