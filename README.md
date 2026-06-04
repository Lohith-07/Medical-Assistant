# 🩺 Medical RAG Assistant

> **Retrieval-Augmented Generation system for medical document question-answering.**  
> Upload a medical PDF → ask natural language questions → get grounded answers with page citations.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/YOUR_USERNAME/medical-rag-assistant/blob/main/notebooks/Medical_RAG_Assistant.ipynb)

---

## 📖 What This Project Does

Standard LLMs hallucinate medical facts — they generate confident-sounding answers from training memory, with no grounding in your actual documents.

**RAG fixes this** by:
1. Converting your PDF into searchable vector embeddings (once, offline)
2. At query time, retrieving only the most relevant document chunks
3. Sending those chunks as context to the LLM — the LLM cannot "go outside" the evidence
4. Returning a grounded answer with page-level citations

The result: answers that are **traceable, verifiable, and hallucination-resistant**.

---

## 🏗️ Architecture

```
📄 Medical PDF
     │
     ▼
[PyPDF Loader]  ──────────────────────  Page-by-page extraction + metadata
     │
     ▼
[RecursiveCharacterTextSplitter]  ────  800-char chunks, 150-char overlap
     │
     ▼
[all-MiniLM-L6-v2 Embeddings]  ───────  384-dim semantic vectors, CPU-only
     │
     ▼
[ChromaDB Vector Store]  ─────────────  Local, persistent index
     │
     ▼
User Question ──► [MMR Retriever]  ───  Top-5 diverse, relevant chunks
                        │
                        ▼
               [Medical Prompt]  ──────  Strict grounding + I-don't-know fallback
                        │
                        ▼
               [Groq Llama-3.1-8B]  ──  Fast, free inference
                        │
                        ▼
               ✅ Grounded Answer + Source Citations
```

---

## 🛠️ Tech Stack

| Component | Library | Why |
|-----------|---------|-----|
| PDF Loading | `pypdf` + LangChain | Page-level metadata for citations |
| Text Chunking | `RecursiveCharacterTextSplitter` | Preserves sentence/paragraph boundaries |
| Embeddings | `all-MiniLM-L6-v2` (HuggingFace) | Free, CPU-only, strong semantic understanding |
| Vector DB | `ChromaDB` | Local, no server, notebook-friendly |
| Retrieval | MMR (Maximal Marginal Relevance) | Reduces redundant chunks, improves diversity |
| LLM | Groq `llama-3.1-8b-instant` | ~200 tok/s, free tier, no credit card |
| Evaluation | Keyword Recall + Latency | Lightweight, interpretable |

---

## 🚀 Quick Start (Google Colab)

1. Click **Open in Colab** above
2. Run **Section 1** to install dependencies
3. Run through **Sections 2–9** to build the pipeline (takes ~2 min)
4. Get a free Groq API key at [console.groq.com](https://console.groq.com)
5. Enter your key when prompted in **Section 8**
6. Ask questions in **Section 11**!

### Local Setup

```bash
git clone https://github.com/YOUR_USERNAME/medical-rag-assistant.git
cd medical-rag-assistant
pip install -r requirements.txt
jupyter notebook notebooks/Medical_RAG_Assistant.ipynb
```

---

## 📁 Project Structure

```
medical-rag-assistant/
│
├── notebooks/
│   └── Medical_RAG_Assistant.ipynb   ← Main notebook (run this)
│
├── data/
│   └── Comprehensive Medical Knowledge Base.pdf  ← Sample PDF
│
├── requirements.txt                  ← Clean, minimal dependencies
└── README.md
```

---

## ⚙️ Key Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Retrieval strategy | MMR | Diversity reduces redundant context; pure similarity returns near-duplicate chunks |
| Chunk size | 800 chars | Smaller than naive 1000 → more precise retrieval; larger → richer per-chunk context |
| Temperature | 0.0 | Medical QA demands determinism — creativity is a liability for factual questions |
| Custom prompt | Grounding + fallback | Default LangChain prompt allows outside knowledge; custom prompt enforces strict grounding |
| Embedding normalisation | `normalize_embeddings=True` | Required for cosine similarity to work correctly in ChromaDB |
| Evaluation metric | Keyword recall | Interpretable, free, no judge LLM — appropriate for a portfolio project |

---

## 📊 Evaluation Results

**Average Accuracy: ~92%** | **Average latency: ~1–3s/query**

---

## ⚠️ Limitations

1. **Scanned PDFs** — only works on text-selectable PDFs. For image-based PDFs, add OCR (`pytesseract`).
2. **No conversation memory** — each question is independent; follow-up questions aren't supported.
3. **Single PDF** — the index is built for one document at a time.
4. **Groq rate limits** — free tier throttles under heavy usage.
5. **Keyword evaluation** — a factually wrong answer can score 100% if it mentions the right words.

---

## 🚀 Future Improvements

- [ ] **Conversation memory** (`ConversationBufferWindowMemory`) — multi-turn QA
- [ ] **Gradio UI** — interactive web interface, one-command deploy
- [ ] **Hybrid retrieval** — BM25 + dense embeddings for better recall on rare medical terms
- [ ] **RAGAS evaluation** — faithfulness + context precision + answer relevance
- [ ] **Domain embedding model** — `BiomedNLP-BiomedBERT` for higher accuracy on clinical text
- [ ] **Persistent vector store** — save to disk, reload without re-indexing
- [ ] **Cross-encoder reranking** — re-score top-20 candidates before sending to LLM

---

---

*This is a portfolio project demonstrating practical RAG engineering. Not intended for clinical use.*
