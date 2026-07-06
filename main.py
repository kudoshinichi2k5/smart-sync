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
STATE_FILE = LOGS / "state.json"
LOG_FILE = LOGS / "latest.log"

def load_state():
    if not STATE_FILE.exists():
        return {}
    with open(STATE_FILE, "r", encoding="utf8") as f:
        return json.load(f)

def save_state(state):
    with open(STATE_FILE, "w", encoding="utf8") as f:
        json.dump(state, f, indent=4)

def write_log(added, updated, skipped):
    text = f"""
    Run Time : {datetime.now()}

    Added    : {added}

    Updated  : {updated}

    Skipped  : {skipped}

    Uploaded : {added+updated}
    """

    with open(LOG_FILE, "w", encoding="utf8") as f:
        f.write(text)
    print(text)


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

    for md in DOCS.glob("*.md"):
        h = file_hash(md)
        if md.name not in old_state:
            added.append(md)

        elif old_state[md.name]["hash"] != h:
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

    for file in updated:
        old_file_id = old_state[file.name]["file_id"]
        delete_file(old_file_id)

    print()

    print("=" * 60)
    print("STEP 4 - UPLOAD")
    print("=" * 60)

    uploaded = upload_files(added + updated)
    new_state = old_state.copy()
    for md in skipped:
        new_state[md.name] = old_state[md.name]

    for md in added + updated:
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
    print("Done.")

if __name__ == "__main__":
    main()