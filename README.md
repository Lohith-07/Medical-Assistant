# 🩺 Medical RAG Assistant

A **Retrieval-Augmented Generation (RAG)** system for medical documents — built with LangChain, ChromaDB, and Google Gemini.

> Upload any medical PDF → ask natural language questions → get grounded answers with page citations.

---

## 🚀 Quick Start (Google Colab)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Lohith-07/Medical-Assistant/blob/main/Medical_RAG_Assistant.ipynb)

1. Click **Open in Colab** above
2. Run **Cell 1** to install dependencies
3. Run **Cell 3** to upload your PDF
4. Enter your **Gemini API key** when prompted → [Get a free key](https://aistudio.google.com/app/apikey)
5. Run all remaining cells and start asking questions!

---

## 🧠 How It Works

```
PDF → Load pages → Split into chunks → Embed (all-MiniLM-L6-v2)
                                              ↓
                                        ChromaDB (vector store)

User Question → Embed query → Similarity search → Top 3 chunks
                                                        ↓
                                          Gemini 2.5 Flash + Prompt
                                                        ↓
                                     Grounded Answer + Page Citations
```

---

## 🛠️ Tech Stack

| Component | Library | Version |
|-----------|---------|---------|
| PDF Parsing | `pypdf` via `langchain-community` | ≥ 4.3 |
| Text Chunking | `langchain` RecursiveCharacterTextSplitter | ≥ 0.3.25 |
| Embeddings | `sentence-transformers` — all-MiniLM-L6-v2 (CPU, free) | ≥ 3.3 |
| Vector Store | `chromadb` (local, no server) | ≥ 1.0 |
| LLM | Google Gemini 2.5 Flash via `langchain-google-genai` | ≥ 2.1.4 |
| RAG Chain | `langchain` RetrievalQA | ≥ 0.3.25 |

---

## 📁 Project Structure

```
Medical RAG/
├── Medical_RAG_Assistant.ipynb   ← Main notebook (run this)
├── data/                         ← Sample medical PDF
│   └── Comprehensive Medical Knowledge Base.pdf
├── requirements.txt              ← Dependencies
└── README.md
```

---

## ⚙️ Key Design Decisions

| Decision | Choice | Why |
|----------|--------|-----|
| Embedding model | `all-MiniLM-L6-v2` | Free, CPU-only, fast, 384-dim vectors |
| Vector DB | ChromaDB | Local, no server, simple setup |
| Chunk size | 1000 chars | Balances context richness vs. retrieval precision |
| Chunk overlap | 200 chars | Prevents losing context at boundaries |
| Top-K | 3 chunks | Enough context without overloading the prompt |
| Temperature | 0 | Deterministic, factual answers for medical use |
| Chain type | `stuff` | Simplest approach — all chunks in one prompt |

---

## ⚠️ Limitations

- **Scanned PDFs** won't work — text must be selectable (not image-based)
- **No conversation memory** — each question is answered independently
- Free Gemini API tier has rate limits
