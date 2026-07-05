import json
from pathlib import Path
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

def create_vector_store():
    """
    Run ONLY once.
    """

    print("Creating Vector Store...")

    store = client.vector_stores.create(
        name="OptiSigns Knowledge Base"
    )

    print(f"Vector Store ID: {store.id}")

    save_state(store.id)

    return store.id


def load_vector_store_id():

    if not STATE_FILE.exists():
        raise RuntimeError(
            "Vector Store not found. Run create_vector_store() first."
        )

    with open(STATE_FILE, "r") as f:
        data = json.load(f)

    return data["vector_store_id"]


def save_state(vector_store_id):

    with open(STATE_FILE, "w") as f:

        json.dump(
            {
                "vector_store_id": vector_store_id
            },
            f,
            indent=4
        )


# =====================================================
# Upload
# =====================================================

def upload_files(files):

    """
    files = list[Path]
    """

    if len(files) == 0:

        print("No files need uploading.")

        return

    vector_store_id = load_vector_store_id()

    print(f"\nUploading {len(files)} changed files...")

    streams = [
        open(file, "rb")
        for file in files
    ]

    batch = client.vector_stores.file_batches.upload_and_poll(
        vector_store_id=vector_store_id,
        files=streams
    )

    print("\nUpload completed.")
    print(f"Status: {batch.status}")
    print(batch.file_counts)

    for s in streams:
        s.close()


# =====================================================
# Standalone Test
# =====================================================

if __name__ == "__main__":

    files = sorted(DOCS_DIR.glob("*.md"))

    upload_files(files)

    print("\nDone.")