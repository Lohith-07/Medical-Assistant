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

## 💬 Interview Q&A (10+ LPA Target)

#### Q1: Why did you choose `RecursiveCharacterTextSplitter` over `CharacterTextSplitter`?
> **Answer**: `CharacterTextSplitter` splits strictly on a single separator (like `\n`). If a paragraph doesn't have that exact separator, it can produce huge chunks that exceed our target size. `RecursiveCharacterTextSplitter` uses a list of separators recursively (starting with paragraph breaks `\n\n`, then newlines `\n`, then spaces ` `, and finally individual characters). This ensures that sentences and paragraphs are kept together as much as possible, preserving semantic integrity.

#### Q2: How does the application prevent hallucinations, especially in a critical field like medicine?
> **Answer**: We enforce two lines of defense:
> 1. **Prompt Engineering**: The system prompt explicitly instructs the LLM: *"Answer the question using ONLY the provided clinical context. If the context does not contain enough information, clearly state 'I cannot answer this based on the provided document.' Never make up facts."*
> 2. **Low Temperature**: We configure the Gemini LLM with a low temperature (`temperature=0.1`). This minimizes creativity and forces the model to be highly deterministic and literal in its generation.

#### Q3: Why did you choose a local embedding model like `all-MiniLM-L6-v2` instead of OpenAI's or Google's embedding APIs?
> **Answer**: Choosing a local embedding model offers three main advantages:
> 1. **Zero Cost**: Embedding APIs charge per token. A local model runs completely free on the client's host CPU.
> 2. **Privacy**: Medical documents contain sensitive information. Local embedding ensures the raw text is not sent to external APIs during vectorization.
> 3. **Offline Performance**: It removes network latency when indexing documents.

#### Q4: How does ChromaDB persist data, and how does your app avoid re-indexing the PDF on every user click?
> **Answer**: 
> 1. **Persistence**: ChromaDB is initialized with a `persist_directory="db"`. When `from_documents` is called, it writes the vector index files and metadata mappings directly to disk in sqlite/parquet format.
> 2. **Session State Cache**: Streamlit runs the script from top to bottom on every user interaction. To avoid re-processing the PDF or reloading the database, we cache the database retriever in `st.session_state.retriever`. We only re-run the ingestion pipeline if a brand new file is uploaded (`st.session_state.uploaded_filename != uploaded_file.name`).

#### Q5: If your medical guidelines PDF is updated, how does your RAG system handle it?
> **Answer**: Since our RAG pipeline retrieves information dynamically at query time from the vector database, we simply clear the `db/` database directory and run the ingestion pipeline on the updated PDF. The new chunks and embeddings will overwrite the database, and the assistant will immediately start using the new guidelines without needing any code changes or model retraining.
