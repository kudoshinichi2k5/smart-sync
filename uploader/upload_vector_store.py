from pathlib import Path
from google import genai
from config import API_KEY
from config import DOCS_DIR

client = genai.Client(
    api_key=API_KEY
)

uploaded = []

for file in sorted(DOCS_DIR.glob("*.md")):
    print(f"Uploading {file.name}")
    f = client.files.upload(
        file=file
    )
    uploaded.append(f)

print()
print("=" * 40)
print(f"Uploaded {len(uploaded)} files")
print("=" * 40)
for f in uploaded:
    print(f.name)