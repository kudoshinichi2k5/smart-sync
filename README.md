# Smart Sync

A lightweight knowledge synchronization pipeline for ingesting support documentation into an OpenAI Vector Store.

The project automatically scrapes OptiSigns Help Center articles, converts them into clean Markdown, uploads them into an OpenAI Vector Store, and keeps the knowledge base synchronized through a scheduled daily workflow.

---

# Features

- Scrape support articles directly from the OptiSigns Zendesk API
- Convert HTML articles into clean Markdown
- Preserve:
  - headings
  - code blocks
  - hyperlinks
- Remove navigation bars and unnecessary HTML
- Detect newly added articles
- Detect updated articles using SHA256 hashing
- Upload only changed documents
- Automatically synchronize every day
- Store documents inside an OpenAI Vector Store
- Generate execution logs
- Dockerized for one-command execution
- GitHub Actions scheduled workflow

---

# Project Architecture

```

OptiSigns Help Center
(Zendesk API)

↓

Fetch Articles

↓

Convert HTML → Markdown

↓

Save Markdown Files

↓

Hash Comparison

↓

Added / Updated ?

↓

Upload Delta Files

↓

OpenAI Vector Store

↓

OpenAI Assistant

```

Only newly added or modified documents are uploaded, reducing embedding costs and avoiding unnecessary API calls.

---

# Project Structure

```

smart-sync/
│
├── docs/
│       Markdown articles
│
├── logs/
│       latest.log
│       state.json
│
├── screenshots/
│       assistant_answer.png
│       openai_vector_store.png
│       github_action_success.png
│       github_action_logs.png
│       docker_run.png
│
├── scraper/
│       fetch_articles.py
│       hash_utils.py
│
├── uploader/
│       upload_vector_store.py
│
├── .github/
│   └── workflows/
│           daily.yml
│
├── Dockerfile
├── requirements.txt
├── main.py
├── config.py
└── README.md

```

---

# Technology Stack

- Python
- OpenAI API
- OpenAI Vector Store
- Requests
- Markdownify
- Docker
- GitHub Actions

---

# Environment Variables

Create a `.env` file.

```

OPENAI_API_KEY=your_openai_api_key
VECTOR_STORE_ID=your_vector_store_id

```

Example

```

OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxx
VECTOR_STORE_ID=vs_xxxxxxxxxxxxx

```

---

# Installation

Clone the repository

```bash
git clone https://github.com/kudoshinichi2k5/smart-sync.git
cd smart-sync
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# Running Locally

Run the entire synchronization pipeline.

```bash
python main.py
```

Example output

```

============================================================
STEP 1 - SCRAPING
============================================================

Found 30+ articles

============================================================
STEP 2 - CHECK DELTA
============================================================

Added : 0
Updated : 1
Skipped : 34

============================================================
STEP 3 - UPLOAD
============================================================

Upload completed.

Done.

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
-e OPENAI_API_KEY=YOUR_API_KEY \
-e VECTOR_STORE_ID=YOUR_VECTOR_STORE_ID \
smart-sync
```

The container performs one synchronization and exits successfully.

---

# Daily Synchronization

The project uses **GitHub Actions** to perform automatic synchronization.

Workflow

```

.github/workflows/daily.yml

```

The workflow performs:

1. Checkout repository
2. Install dependencies
3. Run Smart Sync
4. Detect new articles
5. Upload only delta documents
6. Update synchronization state
7. Commit updated state
8. Upload execution log as workflow artifact

---

# Chunking Strategy

This project uses the default OpenAI Vector Store chunking strategy.

The default OpenAI chunking strategy was selected because it provides a good balance between retrieval quality and implementation simplicity for this project.

---

# OpenAI Assistant

System Prompt

```

You are OptiBot, the customer-support bot for OptiSigns.com.

• Tone: helpful, factual, concise.
• Only answer using the uploaded docs.
• Max 5 bullet points; else link to the doc.
• Cite up to 3 "Article URL:" lines per reply.

```



# Screenshots

## Assistant Answer

The assistant answers questions using the uploaded knowledge base and provides citations from the corresponding documentation.

![Assistant Answer](screenshots/assistant_answer.png)

---

## OpenAI Vector Store

All Markdown documents are successfully uploaded into the OpenAI Vector Store.

![OpenAI Vector Store](screenshots/openai_vector_store.png)

---

## Docker Execution

The Docker container performs one synchronization and exits successfully.

![Docker Execution](screenshots/docker_run.png)

## GitHub Actions Workflow

The scheduled workflow executes successfully on GitHub Actions.

![GitHub Actions](screenshots/github_action_success.png)

# Execution Logs

Example

```

Run Time : 2026-07-05 22:05:31

Added : 0

Updated : 1

Skipped : 34

Uploaded : 1

```

Logs are generated at

```

logs/latest.log

```

Synchronization state is stored in

```

logs/state.json

```

---

# Repository Notes

- No API keys are hard-coded.
- Configuration is provided through environment variables.
- Only changed articles are uploaded.
- The Vector Store is reused across executions.
- The synchronization state is persisted for future runs.

---

# Future Improvements

Possible enhancements include:

- Parallel article downloading
- Custom chunking strategy
- Automatic deletion of removed articles
- Retry mechanism for API failures
- Support for multiple knowledge bases
- Better monitoring and alerting

---

# Author
Le Trung Kien
University of Information Technology (UIT)
Computer Networks and Communications
