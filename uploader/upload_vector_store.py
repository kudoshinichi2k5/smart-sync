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

def create_vector_store():
    print("Creating Vector Store...")

    store = client.vector_stores.create(
        name="OptiSigns Knowledge Base"
    )
    print(f"Vector Store ID: {store.id}")

    return store.id


def upload_all_files(vector_store_id):
    markdown_files = sorted(DOCS_DIR.glob("*.md"))

    streams = [
        open(file, "rb")
        for file in markdown_files
    ]

    print(f"\nUploading {len(streams)} markdown files...")

    batch = client.vector_stores.file_batches.upload_and_poll(
        vector_store_id=vector_store_id,
        files=streams
    )

    print("\nUpload Finished")
    print(batch.status)
    print(batch.file_counts)

    for s in streams:
        s.close()


def save_state(vector_store_id):
    with open(STATE_FILE, "w") as f:
        json.dump(
            {
                "vector_store_id": vector_store_id
            },
            f,
            indent=4,
        )


if __name__ == "__main__":
    vector_store_id = create_vector_store()
    upload_all_files(vector_store_id)
    save_state(vector_store_id)

    print("\nDone.")