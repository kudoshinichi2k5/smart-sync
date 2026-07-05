import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
DOCS_DIR = BASE_DIR / "docs"
LOG_DIR = BASE_DIR / "logs"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")