#!/usr/bin/env python3
"""Entrypoint: copy entry.png to the grader output directory.

Standard library only. Verifies the PNG magic bytes, the 1024x1024
size from the IHDR chunk, and that the copied file is byte-identical
to the source next to this file.
"""

import hashlib
import os
import shutil
import struct
import sys


def png_size(path):
    with open(path, "rb") as handle:
        head = handle.read(33)
    if len(head) < 33 or head[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG file")
    if head[12:16] != b"IHDR":
        raise ValueError("missing IHDR chunk")
    width, height = struct.unpack(">II", head[16:24])
    return width, height


def file_hash(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        print("MAKEFUN_OUTPUT_DIR is not set", file=sys.stderr)
        return 2
    if not os.path.isfile(source):
        print(f"missing source: {source}", file=sys.stderr)
        return 2
    width, height = png_size(source)
    if (width, height) != (1024, 1024):
        print(f"bad size: {width}x{height}, expected 1024x1024", file=sys.stderr)
        return 1
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    shutil.copyfile(source, target)
    source_bytes = os.path.getsize(source)
    target_bytes = os.path.getsize(target)
    if source_bytes != target_bytes:
        print(f"copy mismatch: {source_bytes} vs {target_bytes} bytes", file=sys.stderr)
        return 1
    if file_hash(source) != file_hash(target):
        print("copy mismatch: hashes differ", file=sys.stderr)
        return 1
    print(f"verified entry.png 1024x1024 {target_bytes} bytes sha256={file_hash(target)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
