import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Tự động tìm và nạp file .env từ thư mục gốc
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=BASE_DIR / ".env")

# Lấy trực tiếp GEMINI_API_KEY từ file .env
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("Không tìm thấy GEMINI_API_KEY trong file .env!")

client = genai.Client(api_key=api_key)

DOCS_DIR = BASE_DIR / "docs"

def load_context_from_local_md():
    context_str = ""
    md_files = list(DOCS_DIR.glob("*.md"))
    print(f"Loading content from {len(md_files)} local Markdown files...")
    
    for filepath in md_files:
        with open(filepath, "r", encoding="utf8") as f:
            # Gộp toàn bộ nội dung file vào một chuỗi văn bản lớn làm Context
            context_str += f"\n--- FILE: {filepath.name} ---\n"
            context_str += f.read() + "\n"
            
    return context_str

# 1. Thu thập toàn bộ tri thức từ các bài viết cấu trúc Markdown sạch
knowledge_context = load_context_from_local_md()

# 2. Định nghĩa nguyên văn System Prompt của đề bài
system_instruction = """You are OptiBot, the customer-support bot for OptiSigns.com.
• Tone: helpful, factual, concise.
• Only answer using the uploaded docs.
• Max 5 bullet points; else link to the doc.
• Cite up to 3 "Article URL:" lines per reply."""

# 3. Kết hợp Tri thức + Câu hỏi thành một Prompt duy nhất gửi tới LLM
user_question = "How do I add a YouTube video?"

full_prompt = f"""
Use the following documentation context to answer the user's question.

[DOCUMENTATION CONTEXT]
{knowledge_context}
[END OF CONTEXT]

User Question: {user_question}
"""

print(f"Asking OptiBot: '{user_question}'...")
print("-" * 50)

# 4. Gọi Model sinh câu trả lời
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=full_prompt,
    config=types.GenerateContentConfig(
        system_instruction=system_instruction,
        temperature=0.1  # Để mức thấp nhất để ép bot bám sát text, không bịa đặt
    )
)

print(response.text)
print("-" * 50)