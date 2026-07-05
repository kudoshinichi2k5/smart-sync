from pathlib import Path
import hashlib


def file_hash(path: Path):

    h = hashlib.sha256()

    with open(path, "rb") as f:
        while True:

            chunk = f.read(8192)

            if not chunk:
                break

            h.update(chunk)

    return h.hexdigest()