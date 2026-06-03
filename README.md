# 🩺 Medical RAG Assistant

A complete, intermediate-level **Retrieval-Augmented Generation (RAG)** application designed for clinical document query and grounded question answering. Upload medical PDFs (such as clinical guidelines, patient reports, or medical literature), ask natural language questions, and receive professional, hallucination-free answers anchored strictly in the source documents along with precise page-level citations.

---

## 🚀 Tech Stack
* **Frontend**: [Streamlit](https://streamlit.io/) (Clean, responsive web interface)
* **LLM**: [Google Gemini 2.5 Flash](https://deepmind.google/technologies/gemini/) (Fast, high-context generative model)
* **Orchestration**: [LangChain](https://www.langchain.com/) (Modular RAG orchestration and prompt pipelines)
* **Vector Database**: [ChromaDB](https://www.trychroma.com/) (Local, fast, in-process persistent vector database)
* **Embeddings**: [SentenceTransformers (all-MiniLM-L6-v2)](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) (Local, 384-dimensional semantic encoder)
* **PDF Processing**: `pypdf` (via LangChain's `PyPDFLoader`)
* **Environment Management**: `python-dotenv`

---

## 🏗️ Architecture & Data Flow

Below is the step-by-step data flow showing how clinical information is processed and queried:

```text
[PDF Upload]
     │
     ▼
[pdf_loader.py] ───► Page Extraction (Page Content + Page Number Metadata)
     │
     ▼
[chunking.py]   ───► Recursive Character Splitting (700 chars size, 100 chars overlap)
     │
     ▼
[embeddings.py] ───► SentenceTransformers all-MiniLM-L6-v2 (384-D Local Vector Generation)
     │
     ▼
[vector_store.py]──► ChromaDB Storage (Local persistence in db/ folder)
     │
     ▼
[retriever.py]  ───► Similarity Search (Calculates Cosine Similarity for top k chunks)
     │
     ▼
[rag_chain.py]  ───► Context formatting & Gemini Prompt Injection
     │
     ▼
[Gemini 2.5 LLM]───► Grounded Response Generation
     │
     ▼
[Streamlit UI]  ───► Answer Display & Citation Card References (Source Name & Page)
```

---

## 🧠 Core Concepts Explained (Placement Prep)

### 1. Why use RAG (Retrieval-Augmented Generation)?
Large Language Models (LLMs) are trained on public data up to a specific cutoff date. They have two major limitations:
* **Knowledge Cutoff**: They cannot answer questions about your private or newly released documents.
* **Hallucinations**: When asked about specific, niche details, LLMs might confidently generate false facts. This is dangerous in the medical field.

**RAG** solves this by retrieving the exact relevant pages of your uploaded document first, pasting them directly into the prompt as a "cheat sheet," and instructing the LLM to write its response *only* using that retrieved context.

### 2. What are Text Embeddings?
Embeddings are high-dimensional numerical vectors (lists of floats) representing the *semantic meaning* of a piece of text. 
* Our local model, `all-MiniLM-L6-v2`, represents text in a **384-dimensional** space.
* If two texts have similar meanings (e.g., "high blood glucose" and "hyperglycemia"), their vectors will point in nearly the same direction.
* We measure this closeness using **Cosine Similarity** (a mathematical measure of the angle between two vectors).

### 3. What is a Vector Database?
Traditional databases query tables by exact keyword matches. A vector database like **ChromaDB** stores embeddings (vectors) and indexing configurations. It is optimized to perform high-speed, nearest-neighbor vector search, letting us find the top `k` most semantically similar text blocks in milliseconds.

### 4. What is Text Chunking?
A full medical document contains thousands of words. Passing the whole PDF to the LLM increases latency, costs, and introduces noise. 
* We break documents into **chunks** using a `RecursiveCharacterTextSplitter`.
* We set `chunk_size = 700` (ideal length for containing complete paragraphs or ideas).
* We set `chunk_overlap = 100` characters. Overlap ensures that if a key sentence gets split at a chunk boundary, the context is preserved in both adjacent chunks, avoiding loss of information.

### 5. What is Semantic Retrieval?
When a user asks a question:
1. The question is converted into a 384-D vector using the same local embedding model.
2. The retriever queries the vector database for the top 3 most similar document chunks.
3. These chunks, along with their metadata (such as page number), are sent to the LLM as context.

---

## 🛠️ Installation & Setup

Follow these steps to run the application locally on Windows:

### 1. Clone the Project & Open Folder
Make sure you are in the project root directory:
```powershell
cd "d:\Edu\Project\Medical RAG"
```

### 2. Configure Environment Variables
Open the `.env` file in the root directory and replace the placeholder with your actual Gemini API key:
```text
GEMINI_API_KEY=AIzaSyYourActualAPIKeyHere
```

### 3. Activate Virtual Environment
```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Run the Streamlit Application
```powershell
streamlit run app.py
```
This will open the application in your default web browser (usually at `http://localhost:8501`).

---
