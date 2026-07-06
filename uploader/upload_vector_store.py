import json
from openai import OpenAI

from config import DOCS_DIR
from config import OPENAI_API_KEY
from config import BASE_DIR

client = OpenAI(api_key=OPENAI_API_KEY)

STATE_DIR = BASE_DIR / "state"
STATE_DIR.mkdir(exist_ok=True)

STATE_FILE = STATE_DIR / "vector_store.json"


# =====================================================
# Vector Store Utilities
# =====================================================
def load_vector_store_id():
    """
    Load existing Vector Store.
    If it doesn't exist, create a new one automatically.
    """

    if not STATE_FILE.exists():
        print("Vector Store not found.")
        print("Creating a new one...\n")
        return create_vector_store()

    with open(STATE_FILE, "r", encoding="utf8") as f:
        data = json.load(f)

    return data["vector_store_id"]


# =====================================================
# Upload Files
# =====================================================

def upload_files(files):
    """
    Upload a list of markdown files to OpenAI Vector Store.

    Args:
        files (list[Path])
    """

    if len(files) == 0:
        print("No files need uploading.")
        return

    vector_store_id = load_vector_store_id()

    print(f"\nUploading {len(files)} file(s)...")

    streams = []

    try:

        for file in files:
            streams.append(open(file, "rb"))

        batch = client.vector_stores.file_batches.upload_and_poll(
            vector_store_id=vector_store_id,
            files=streams
        )

        print("\nUpload completed.")
        print(f"Status : {batch.status}")
        print(f"Files  : {batch.file_counts}")

    finally:

        for s in streams:
            s.close()


# =====================================================
# Standalone Test
# =====================================================

if __name__ == "__main__":

    markdown_files = sorted(DOCS_DIR.glob("*.md"))

    upload_files(markdown_files)

    print("\nDone.")