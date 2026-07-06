import json
from pathlib import Path
from datetime import datetime

from scraper.fetch_articles import main as scrape
from scraper.hash_utils import file_hash

from uploader.upload_vector_store import (
    upload_files,
    delete_file
)

BASE_DIR = Path(__file__).resolve().parent

DOCS = BASE_DIR / "docs"

LOGS = BASE_DIR / "logs"
LOGS.mkdir(exist_ok=True)

STATE_FILE = LOGS / "state.json"
LOG_FILE = LOGS / "latest.log"


# =====================================================
# State
# =====================================================

def load_state():

    if not STATE_FILE.exists():
        return {}

    with open(STATE_FILE, "r", encoding="utf8") as f:
        return json.load(f)


def save_state(state):

    with open(STATE_FILE, "w", encoding="utf8") as f:
        json.dump(
            state,
            f,
            indent=4
        )


# =====================================================
# Log
# =====================================================

def write_log(added, updated, skipped):

    text = f"""
Run Time : {datetime.now()}

Added    : {added}

Updated  : {updated}

Skipped  : {skipped}

Uploaded : {added + updated}
"""

    with open(LOG_FILE, "w", encoding="utf8") as f:
        f.write(text)

    print(text)


# =====================================================
# Main
# =====================================================

def main():

    print("=" * 60)
    print("STEP 1 - SCRAPING")
    print("=" * 60)

    scrape()

    print()

    print("=" * 60)
    print("STEP 2 - DELTA DETECTION")
    print("=" * 60)

    old_state = load_state()

    added = []
    updated = []
    skipped = []

    for md in sorted(DOCS.glob("*.md")):

        current_hash = file_hash(md)

        old = old_state.get(md.name)

        if old is None:

            added.append(md)

        elif old["hash"] != current_hash:

            updated.append(md)

        else:

            skipped.append(md)

    print(f"Added   : {len(added)}")
    print(f"Updated : {len(updated)}")
    print(f"Skipped : {len(skipped)}")

    print()

    print("=" * 60)
    print("STEP 3 - REMOVE OLD FILES")
    print("=" * 60)

    for md in updated:

        old = old_state.get(md.name)

        if old and "file_id" in old:

            delete_file(old["file_id"])

    print()

    print("=" * 60)
    print("STEP 4 - UPLOAD")
    print("=" * 60)

    changed = added + updated

    uploaded = {}

    if changed:

        uploaded = upload_files(changed)

    else:

        print("No changed files.")

    print()

    print("=" * 60)
    print("STEP 5 - SAVE STATE")
    print("=" * 60)

    new_state = {}

    # giữ nguyên file không đổi
    for md in skipped:

        new_state[md.name] = old_state[md.name]

    # cập nhật file mới
    for md in changed:

        new_state[md.name] = {

            "hash": file_hash(md),

            "file_id": uploaded[md.name]["file_id"]

        }

    save_state(new_state)

    write_log(

        len(added),

        len(updated),

        len(skipped)

    )

    print()

    print("Done.")


if __name__ == "__main__":
    main()