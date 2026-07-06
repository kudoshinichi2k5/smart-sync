import json
from openai import OpenAI
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from config import OPENAI_API_KEY
from config import BASE_DIR

client = OpenAI(api_key=OPENAI_API_KEY)

STATE_DIR = BASE_DIR / "state"
STATE_DIR.mkdir(exist_ok=True)
STATE_FILE = STATE_DIR / "vector_store.json"

def main():
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

    print(f"Vector Store created: {store.id}")
    print("Saved to state/vector_store.json")

if __name__ == "__main__":
    main()