import json
from pathlib import Path
from openai import OpenAI
from config import BASE_DIR
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

STATE_FILE = BASE_DIR / "state" / "vector_store.json"
with open(STATE_FILE, "r") as f:
    vector_store_id = json.load(f)["vector_store_id"]

SYSTEM_PROMPT = """
You are OptiBot, the customer-support bot for OptiSigns.com.

Tone:
- helpful
- factual
- concise

Rules:
- Only answer using the uploaded docs.
- Maximum 5 bullet points.
- If the answer is long, summarize and recommend the related article.
- Cite up to 3 Article URL lines whenever possible.
"""


question = "How do I add a YouTube video?"

response = client.responses.create(
    model="gpt-5-mini",
    input=[
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": question,
        },
    ],
    tools=[
        {
            "type": "file_search",
            "vector_store_ids": [vector_store_id],
        }
    ],
)

print("=" * 60)
print("QUESTION")
print("=" * 60)
print(question)

print("\n")

print("=" * 60)
print("ANSWER")
print("=" * 60)
print(response.output_text)