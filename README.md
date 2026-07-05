# Smart Sync

A mini knowledge ingestion pipeline that scrapes OptiSigns Help Center articles, converts them into clean Markdown, uploads them to an OpenAI Vector Store, and keeps the knowledge base synchronized through a scheduled daily job.

---

## Project Overview

This project was built as part of the OptiBot Mini-Clone Take-Home Test.

Pipeline:

```
OptiSigns Help Center
        │
        ▼
 Scrape Articles (Zendesk API)
        │
        ▼
 Convert HTML → Markdown
        │
        ▼
 Detect Added / Updated Articles
        │
        ▼
 Upload Delta Files
        │
        ▼
 OpenAI Vector Store
        │
        ▼
 OpenAI Assistant
```

The pipeline only uploads newly added or modified documents, reducing unnecessary embedding costs.

---

# Project Structure

```
smart-sync/
│
├── docs/                    # Markdown articles
├── logs/                    # Latest execution logs
├── scraper/
│   ├── fetch_articles.py
│   ├── hash_utils.py
│   └── ...
│
├── uploader/
│   ├── config.py
│   └── upload_vector_store.py
│
├── state/
│   └── vector_store.json
│
├── .github/workflows/
│   └── daily.yml
│
├── Dockerfile
├── requirements.txt
├── main.py
└── README.md
```

---

# Features

- Scrape 35 OptiSigns support articles via Zendesk API
- Convert HTML into clean Markdown
- Preserve:
  - headings
  - code blocks
  - links
- Remove navigation and unnecessary HTML
- Detect newly added articles
- Detect updated articles using SHA256 hash
- Upload only changed files
- Store documents in OpenAI Vector Store
- Automatically synchronize every day using GitHub Actions
- Generate execution logs

---

# Requirements

Python 3.11+

Install dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env`

```
OPENAI_API_KEY=your_api_key
```

Example

```
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxx
```

---

# Run Locally

Run the complete pipeline

```bash
python main.py
```

Pipeline execution

```
STEP 1
Scrape articles

STEP 2
Detect delta

STEP 3
Upload changed files

Done
```

---

# Docker

Build

```bash
docker build -t smart-sync .
```

Run

```bash
docker run \
-e OPENAI_API_KEY=YOUR_KEY \
smart-sync
```

The container runs once and exits successfully.

---

# Daily Job

GitHub Actions is used to schedule the synchronization job.

Workflow

```
.github/workflows/daily.yml
```

Schedule

```
Every day
```

The workflow:

- Scrapes articles
- Detects delta
- Uploads changed files
- Saves execution logs

Execution logs are available in:

```
GitHub Actions
→ Artifacts
→ latest-log.zip
```

---

# Chunking Strategy

The project uses the default OpenAI Vector Store chunking strategy.

Reason:

- optimized for Retrieval-Augmented Generation
- preserves semantic context
- no manual tuning required for this project

---

# Assistant

System Prompt

```
You are OptiBot, the customer-support bot for OptiSigns.com.

• Tone: helpful, factual, concise.
• Only answer using the uploaded docs.
• Max 5 bullet points; else link to the doc.
• Cite up to 3 "Article URL:" lines per reply.
```

Example Question

```
How do I add a YouTube video?
```

See the screenshot below.

```
/screenshots/assistant_answer.png
```

---

# Logs

Example

```
Run Time : 2026-07-05 22:05

Added : 0

Updated : 1

Skipped : 34

Uploaded : 1
```

---

# Technologies

- Python
- OpenAI API
- OpenAI Vector Store
- Markdownify
- Requests
- Docker
- GitHub Actions

---

