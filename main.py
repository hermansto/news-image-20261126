#!/usr/bin/env python3
"""Deliver the finished front page for 26 November 2026.

The picture itself is drawn ahead of time by draw.py (run on the
author's machine) and stored in this repository as entry.png. This program is the part the grader executes, and the
grader installs nothing, so it uses only the Python standard
library: it copies entry.png into the output directory and checks
the copy byte for byte.

It writes one file only: $MAKEFUN_OUTPUT_DIR/entry.png
(default /output). It never writes into the repository, never
touches the network, and always produces the same bytes.
"""

import hashlib
import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
EXPECTED_SIZE = (1024, 1024)


def fail(message):
    print("error: " + message, file=sys.stderr)
    return 1


def read_png(path):
    with open(path, "rb") as handle:
        blob = handle.read()
    if not blob.startswith(PNG_MAGIC):
        return None, "not a PNG file: " + path
    width, height = struct.unpack(">II", blob[16:24])
    if (width, height) != EXPECTED_SIZE:
        return None, "entry.png is %dx%d, expected 1024x1024" % (
            width, height)
    return blob, None


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    blob, problem = read_png(SOURCE)
    if problem:
        return fail(problem)
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SOURCE, dest)
    copied, problem = read_png(dest)
    if problem:
        return fail("output failed checks: " + problem)
    if copied != blob:
        return fail("copied entry.png differs from the repository copy")
    print("wrote " + dest)
    print("size: 1024x1024")
    print("bytes: %d" % len(blob))
    print("sha256: " + hashlib.sha256(blob).hexdigest())
    print("verified: output matches the repository entry.png byte for byte")
    return 0


if __name__ == "__main__":
    sys.exit(main())
