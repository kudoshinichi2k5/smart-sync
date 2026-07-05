from pathlib import Path

import requests
from markdownify import markdownify as md
from tqdm import tqdm

BASE_URL = "https://support.optisigns.com"
API_URL = f"{BASE_URL}/api/v2/help_center/en-us/articles.json"

HEADERS = {
    "User-Agent": "smart-sync/1.0"
}

BASE_DIR = Path(__file__).resolve().parent.parent
DOCS_DIR = BASE_DIR / "docs"
DOCS_DIR.mkdir(parents=True, exist_ok=True)

MAX_ARTICLES = 35


def get_all_articles():
    articles = []
    next_page = API_URL

    while next_page and len(articles) < MAX_ARTICLES:
        print(f"Fetching {next_page}")

        response = requests.get(
            next_page,
            headers=HEADERS,
            timeout=30
        )
        response.raise_for_status()

        data = response.json()

        remaining = MAX_ARTICLES - len(articles)

        articles.extend(data["articles"][:remaining])

        next_page = data["next_page"]

    return articles


def clean_html(html: str) -> str:
    return md(
        html,
        heading_style="ATX"
    ).strip()


def save_article(article):
    title = article["title"]

    slug = article["html_url"].rstrip("/").split("/")[-1]

    raw_body = article.get("body") or ""

    body = clean_html(raw_body)

    filepath = DOCS_DIR / f"{slug}.md"

    with open(filepath, "w", encoding="utf8") as f:
        f.write(f"# {title}\n\n")
        f.write(f"Article URL: {article['html_url']}\n")
        f.write(f"Last Updated: {article['updated_at']}\n")
        f.write("\n---\n\n")
        f.write(body)

    print(f"Saved {filepath.name}")


def main():
    articles = get_all_articles()

    print(f"\nDownloaded {len(articles)} articles\n")

    for article in tqdm(articles):
        save_article(article)

    print("\nDone.")


if __name__ == "__main__":
    main()