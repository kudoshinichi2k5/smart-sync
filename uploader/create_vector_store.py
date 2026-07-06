from openai import OpenAI
import json
from pathlib import Path
from config import OPENAI_API_KEY, BASE_DIR
client = OpenAI(api_key=OPENAI_API_KEY)

STATE_DIR = BASE_DIR / "state"
STATE_DIR.mkdir(exist_ok=True)
STATE_FILE = STATE_DIR / "vector_store.json"


def main():
    print("Creating Vector Store...")
    store = client.vector_stores.create(
        name="OptiSigns Knowledge Base"
    )
    print(f"Vector Store ID: {store.id}")
    with open(STATE_FILE, "w") as f:
        json.dump(
            {
                "vector_store_id": store.id
            },
            f,
            indent=4
        )

    print("Saved to state/vector_store.json")

if __name__ == "__main__":
    main()