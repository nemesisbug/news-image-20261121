#!/usr/bin/env python3
"""The World in One Day - Saturday 21 November 2026.

Deterministic, offline entrypoint: copies the entry image that this
repository holds into the output directory make.fun reads.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
DST = os.path.join(OUT_DIR, "entry.png")


def main():
    with open(SRC, "rb") as fh:
        head = fh.read(4)
    if head != b"\x89PNG":
        raise SystemExit("entry.png is not a PNG file")
    os.makedirs(OUT_DIR, exist_ok=True)
    shutil.copyfile(SRC, DST)
    with open(DST, "rb") as fh:
        copied = fh.read()
    with open(SRC, "rb") as fh:
        original = fh.read()
    if copied != original:
        raise SystemExit("entry.png copy differs from source")
    print(f"wrote {DST} ({len(copied)} bytes)")


if __name__ == "__main__":
    main()
