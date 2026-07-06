import json
from pathlib import Path
from datetime import datetime

from scraper.fetch_articles import main as scrape
from scraper.hash_utils import file_hash
from uploader.upload_vector_store import upload_files

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

        json.dump(
            state,
            f,
            indent=4
        )

def write_log(added, updated, skipped):

    text = f"""
    Run Time : {datetime.now()}
    Added : {added}
    Updated : {updated}
    Skipped : {skipped}
    Uploaded : {added + updated}
    """

    with open(LOG_FILE, "w") as f:

        f.write(text)

    print(text)

def main():

    print("="*60)
    print("STEP 1 - SCRAPING")
    print("="*60)

    scrape()

    print()

    print("="*60)
    print("STEP 2 - CHECK DELTA")
    print("="*60)

    state = load_state()
    added = []
    updated = []
    skipped = []
    new_state = {}

    for md in DOCS.glob("*.md"):
        h = file_hash(md)
        new_state[md.name] = {
            "hash": h
        }
        old = state.get(md.name)
        if old is None:
            added.append(md)

        elif old["hash"] != h:
            updated.append(md)

        else:
            skipped.append(md)

    changed = added + updated

    print(f"Added   : {len(added)}")
    print(f"Updated : {len(updated)}")
    print(f"Skipped : {len(skipped)}")

    print()

    print("="*60)
    print("STEP 3 - UPLOAD")
    print("="*60)

    if changed:
        upload_files(changed)
        save_state(new_state)

    else:
        print("No changed files.")

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