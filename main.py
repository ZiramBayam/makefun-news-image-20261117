#!/usr/bin/env python3
"""Copy the verified 17 Nov 2026 news illustration into the output directory."""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "entry.png"
OUT_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
MAX_BYTES = 1024 * 1024
MAX_DIM = 1024
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def main() -> None:
    data = SOURCE.read_bytes()
    assert data.startswith(PNG_MAGIC), "not a PNG"
    assert len(data) <= MAX_BYTES, "PNG exceeds 1 MiB"
    # IHDR follows the 8-byte signature + 4-byte length + 4-byte type:
    # bytes 16..20 hold the width and 20..24 the height, both big-endian.
    width = int.from_bytes(data[16:20], "big")
    height = int.from_bytes(data[20:24], "big")
    assert width <= MAX_DIM and height <= MAX_DIM, "dimensions exceed 1024x1024"
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "entry.png").write_bytes(data)


if __name__ == "__main__":
    main()
