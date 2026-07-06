import json
from openai import OpenAI
from config import OPENAI_API_KEY
from config import BASE_DIR

client = OpenAI(api_key=OPENAI_API_KEY)

STATE_DIR = BASE_DIR / "state"
STATE_DIR.mkdir(exist_ok=True)
STATE_FILE = STATE_DIR / "vector_store.json"


# =====================================================
# Vector Store
# =====================================================

def create_vector_store():
    print("Creating Vector Store...")

    store = client.vector_stores.create(
        name="OptiSigns Knowledge Base"
    )

    with open(STATE_FILE, "w", encoding="utf8") as f:
        json.dump(
            {
                "vector_store_id": store.id
            },
            f,
            indent=4
        )

    print("Created:", store.id)

    return store.id


def load_vector_store_id():
    if not STATE_FILE.exists():
        return create_vector_store()

    with open(STATE_FILE, "r", encoding="utf8") as f:
        data = json.load(f)

    return data["vector_store_id"]


# =====================================================
# Upload
# =====================================================

def upload_files(files):
    """
    Upload markdown files.
    Returns
    -------
    {
        filename:{
            "file_id":xxx
        }
    }
    """

    if len(files) == 0:
        return {}

    vector_store_id = load_vector_store_id()
    uploaded = {}

    print(f"\nUploading {len(files)} file(s)...")

    for path in files:
        with open(path, "rb") as f:
            openai_file = client.files.create(
                file=f,
                purpose="assistants"
            )

        client.vector_stores.files.create(
            vector_store_id=vector_store_id,
            file_id=openai_file.id
        )

        uploaded[path.name] = {
            "file_id": openai_file.id
        }

        print(f"Uploaded {path.name}")

    return uploaded


# =====================================================
# Delete old file
# =====================================================

def delete_file(file_id):
    try:
        client.files.delete(file_id)
        print(f"Deleted old file {file_id}")

    except Exception as e:
        print(f"Skip deleting {file_id}: {e}")