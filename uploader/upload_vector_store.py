from pathlib import Path

from openai import OpenAI

from config import DOCS_DIR
from config import OPENAI_API_KEY

client = OpenAI(
    api_key=OPENAI_API_KEY
)

files = sorted(Path(DOCS_DIR).glob("*.md"))

print("=" * 50)
print("OpenAI Connected")
print("=" * 50)

print(f"Found {len(files)} markdown files.\n")

for file in files:
    print(file.name)