#!/usr/bin/env python3
"""Deliver the finished front page to the make.fun output directory.

The entry image is rendered ahead of time by build_image.py and sits next
to this file as entry.png. All this module does is hand that one file to
the harness: it reads $MAKEFUN_OUTPUT_DIR, drops a verified copy of
entry.png there, and refuses to finish unless the copy hashes identically
to the source. Standard library only.
"""

from __future__ import annotations

import hashlib
import os
import shutil
import sys
from pathlib import Path

ENTRY_NAME = "entry.png"
OUTPUT_ENV_VAR = "MAKEFUN_OUTPUT_DIR"


def script_folder() -> Path:
    return Path(__file__).resolve().parent


def fingerprint(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 16), b""):
            digest.update(chunk)
    return digest.hexdigest()


def resolve_destination() -> Path:
    raw = os.environ.get(OUTPUT_ENV_VAR, "")
    if not raw.strip():
        raise SystemExit(
            f"{OUTPUT_ENV_VAR} is not set; "
            "the harness must point it at an output folder first."
        )
    destination = Path(raw).expanduser()
    destination.mkdir(parents=True, exist_ok=True)
    return destination


def hand_over(source: Path, folder: Path) -> Path:
    if not source.is_file():
        raise SystemExit(f"missing entry image: {source}")
    target = folder / ENTRY_NAME
    shutil.copyfile(source, target)
    if fingerprint(source) != fingerprint(target):
        target.unlink(missing_ok=True)
        raise SystemExit(f"copy check failed for {target}; removed bad copy.")
    return target


def run() -> int:
    source = script_folder() / ENTRY_NAME
    folder = resolve_destination()
    delivered = hand_over(source, folder)
    size = delivered.stat().st_size
    print(f"entry delivered: {delivered} ({size} bytes, "
          f"sha256 {fingerprint(delivered)[:16]}...)")
    return 0


if __name__ == "__main__":
    sys.exit(run())
