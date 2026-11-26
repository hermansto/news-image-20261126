#!/usr/bin/env python3
"""Ship the finished 26 November 2026 front page.

The picture is painted ahead of time by draw.py on the author's
machine and kept in this repository as entry.png. This program is
the only part the grader executes, and the grader installs
nothing, so it stays inside the Python standard library: it reads
entry.png, checks that it really is the 1024x1024 PNG this entry
promises, copies it into the output directory, and then reads the
copy back to prove the copy is byte for byte the same file.

It writes exactly one file, $MAKEFUN_OUTPUT_DIR/entry.png
(/output when the variable is unset). It never writes into the
repository, never opens a socket, and always yields the same
bytes, so two runs are identical. A missing output directory is
created first; an existing entry.png there is replaced.
"""

import hashlib
import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_PNG = os.path.join(HERE, "entry.png")
SIGNATURE = b"\x89PNG\r\n\x1a\n"
WANTED = (1024, 1024)


def complain(text):
    print("error: " + text, file=sys.stderr)
    return 1


def load_png(path):
    """Return (bytes, None) for a valid 1024x1024 PNG, else (None, reason)."""
    with open(path, "rb") as handle:
        blob = handle.read()
    if blob[:8] != SIGNATURE:
        return None, "not a PNG file: " + path
    width, height = struct.unpack(">II", blob[16:24])
    if (width, height) != WANTED:
        return None, "entry.png is %dx%d, expected 1024x1024" % (
            width, height)
    return blob, None


def run():
    destination_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    original, problem = load_png(REPO_PNG)
    if problem:
        return complain(problem)
    os.makedirs(destination_dir, exist_ok=True)
    destination = os.path.join(destination_dir, "entry.png")
    shutil.copyfile(REPO_PNG, destination)
    delivered, problem = load_png(destination)
    if problem:
        return complain("output failed checks: " + problem)
    if len(delivered) != len(original):
        return complain("copied entry.png has the wrong length")
    if delivered != original:
        return complain("copied entry.png differs from the repository copy")
    print("wrote " + destination)
    print("size: 1024x1024")
    print("bytes: %d" % len(original))
    print("sha256: " + hashlib.sha256(original).hexdigest())
    print("verified: output matches the repository entry.png byte for byte")
    return 0


if __name__ == "__main__":
    sys.exit(run())
