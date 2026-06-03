# 🩺 Medical RAG Assistant

A **Retrieval-Augmented Generation (RAG)** pipeline for medical documents, built with LangChain, ChromaDB, and Google Gemini.

## What It Does

Upload any clinical PDF → ask natural language questions → get grounded answers with source page citations.

## Project Structure

```
Medical RAG/
├── Medical_RAG_Assistant.ipynb   ← Main notebook (run this)
├── data/                         ← Put your PDF files here
│   └── your_medical_document.pdf
├── .env                          ← API key (never commit this)
├── requirements.txt
└── README.md
```

## Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Add your Gemini API key
Create a `.env` file (already present) and set:
```
GEMINI_API_KEY=AIzaSy...
```
Get a free key at: https://aistudio.google.com/app/apikey

### 3. Add your PDF
Drop any medical PDF into the `data/` folder.

### 4. Run the notebook
```bash
jupyter notebook Medical_RAG_Assistant.ipynb
```
Then run cells **top to bottom**.

---

## Tech Stack

| Component | Library |
|---|---|
| PDF Parsing | `pypdf` via `langchain-community` |
| Text Chunking | `RecursiveCharacterTextSplitter` |
| Embeddings | `sentence-transformers` — `all-MiniLM-L6-v2` (CPU, free) |
| Vector Store | `ChromaDB` (local, no server) |
| LLM | Google Gemini 2.5 Flash |
| Orchestration | `LangChain` |

## RAG Pipeline

```
PDF → Load pages → Split into chunks → Embed (384-dim vectors)
                                              ↓
                                         ChromaDB (stored)

User Question → Embed query → Similarity search → Top-3 chunks
                                                        ↓
                                              Gemini LLM + Prompt
                                                        ↓
                                         Grounded Answer + Page Citations
```

## Key Design Decisions

- **Temperature = 0.1** — minimizes hallucination, critical for medical use
- **Local embeddings** — no API cost, works offline
- **Chunk overlap = 200** — preserves context at chunk boundaries
- **k = 3 retrieved chunks** — balances context richness vs prompt size
