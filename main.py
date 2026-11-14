"""food-picture-01 entry (Python 3.13, standard library only).

The entry ships one picture of food — a photorealistic close-up of a
gourmet smash cheeseburger with molten cheddar dripping down a charred
beef patty, shot in warm golden side light on dark slate — as entry.png
beside this file, and this program copies it byte-for-byte to the
grader's output directory as /output/entry.png.

The copy is deterministic by construction: it reads the shipped file and
writes the exact same bytes, so two runs of this program produce
identical output. No network, no randomness, no time or environment
dependence beyond the output directory itself.

Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for
/output, exactly like the kit's starter:

    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import hashlib
import os
import shutil
import sys
from pathlib import Path

SOURCE_NAME = "entry.png"
DEST_NAME = "entry.png"


def main() -> int:
    here = Path(__file__).resolve().parent
    source = here / SOURCE_NAME

    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    dest = out_dir / DEST_NAME

    if not source.is_file():
        print(f"error: {SOURCE_NAME} not found beside main.py", file=sys.stderr)
        return 1

    out_dir.mkdir(parents=True, exist_ok=True)

    # Copy through a temporary file and rename, so the destination is
    # never observed half-written, then confirm the copy is exact by
    # comparing both size and content hash.
    tmp = dest.with_suffix(".tmp")
    shutil.copyfile(source, tmp)
    os.replace(tmp, dest)

    def digest(path: Path) -> str:
        h = hashlib.sha256()
        with path.open("rb") as f:
            for chunk in iter(lambda: f.read(1 << 20), b""):
                h.update(chunk)
        return h.hexdigest()

    if dest.stat().st_size != source.stat().st_size or digest(dest) != digest(source):
        print("error: copied file differs from source", file=sys.stderr)
        return 1

    print(f"wrote {dest} ({dest.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
