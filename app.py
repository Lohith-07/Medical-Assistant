import os
import streamlit as st
from frontend.ui import setup_page, render_header, render_source_card
from backend.pdf_loader import load_pdf
from backend.chunking import split_documents
from backend.embeddings import get_embedding_model
from backend.vector_store import create_vector_store
from backend.retriever import get_retriever
from backend.rag_chain import get_llm, run_rag_pipeline

# 1. Setup Streamlit page configuration and styling
setup_page()

# 2. Render Page Header
render_header()

# Sidebar - Developer & Technical Dashboard
with st.sidebar:
    st.markdown(
        """
        <div style="text-align: center; padding: 15px 0;">
            <span style="font-size: 3.5rem;">🩺</span>
            <h2 style="margin-top: 10px; color: #1a365d; font-weight: 800; font-size: 1.5rem;">RAG Dashboard</h2>
            <p style="color: #718096; font-size: 0.85rem;">System Parameters & Configuration</p>
        </div>
        <hr style="margin-top: 5px; margin-bottom: 20px; border-color: #e2e8f0;"/>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("### ⚙️ System Stack")
    st.info(
        "**LLM**: `gemini-2.5-flash` (Generative)\n\n"
        "**Embeddings**: `all-MiniLM-L6-v2` (Local, 384-D)\n\n"
        "**Vector DB**: `ChromaDB` (Persistent, Local)"
    )
    
    st.markdown("### 📊 Hyperparameters")
    st.success(
        "**Chunk Size**: 700 characters\n\n"
        "**Chunk Overlap**: 100 characters\n\n"
        "**Retrieval Count (k)**: 3 context chunks"
    )
    
    st.markdown("### 🧠 Interview Insight")
    st.warning(
        "**Why RAG?**\n\n"
        "Retrieval-Augmented Generation solves knowledge-cutoff and prevents hallucinations "
        "by feeding precise context chunks directly into the LLM prompt window, generating "
        "fully grounded medical responses with citations."
    )


# 3. Initialize Streamlit session state variables
if "uploaded_filename" not in st.session_state:
    st.session_state.uploaded_filename = None
if "retriever" not in st.session_state:
    st.session_state.retriever = None
if "num_pages" not in st.session_state:
    st.session_state.num_pages = 0
if "num_chunks" not in st.session_state:
    st.session_state.num_chunks = 0

# 4. Check for Gemini API key and initialize LLM early
api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
if not api_key or api_key == "your_gemini_api_key_here":
    st.warning(
        "⚠️ Gemini API Key is missing. "
        "Please open the `.env` file in the root folder and add your key: "
        "`GEMINI_API_KEY=AIzaSy...`"
    )
    st.info("You can get a free Gemini API key from Google AI Studio.")
    st.stop()  # Stop execution of the app here until the API key is configured

# Initialize LLM instance on every rerun to prevent caching stale model objects
try:
    llm = get_llm()
except Exception as e:
    st.error(f"Failed to initialize Gemini LLM: {e}")
    st.stop()

# Sidebar - Developer & Technical Dashboard
with st.sidebar:
    st.markdown(
        """
        <div style="text-align: center; padding: 15px 0;">
            <span style="font-size: 3.5rem;">🩺</span>
            <h2 style="margin-top: 10px; color: #1a365d; font-weight: 800; font-size: 1.5rem;">RAG Dashboard</h2>
            <p style="color: #718096; font-size: 0.85rem;">System Parameters & Configuration</p>
        </div>
        <hr style="margin-top: 5px; margin-bottom: 20px; border-color: #e2e8f0;"/>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("### ⚙️ System Stack")
    st.info(
        "**LLM**: `gemini-2.5-flash` (Generative)\n\n"
        "**Embeddings**: `all-MiniLM-L6-v2` (Local, 384-D)\n\n"
        "**Vector DB**: `ChromaDB` (Persistent, Local)"
    )
    
    # Active Document Stats
    if st.session_state.retriever is not None and st.session_state.num_pages > 0:
        st.markdown("### 📊 Active Document Stats")
        st.markdown(
            f"- **Pages**: {st.session_state.num_pages}\n"
            f"- **Text Chunks**: {st.session_state.num_chunks}"
        )
    
    st.markdown("### 📊 Hyperparameters")
    st.success(
        "**Chunk Size**: 700 characters\n\n"
        "**Chunk Overlap**: 100 characters\n\n"
        "**Retrieval Count (k)**: 3 context chunks"
    )
    
    # Reset Database control button
    st.markdown("### 🧹 Database Admin")
    if st.button("Clear Vector Store", type="secondary", use_container_width=True):
        try:
            # 1. Delete Chroma DB collection to release handles and clear vectors
            if st.session_state.retriever is not None:
                try:
                    st.session_state.retriever.vectorstore.delete_collection()
                except Exception:
                    pass
            
            # 2. Reset session state variables
            st.session_state.uploaded_filename = None
            st.session_state.retriever = None
            st.session_state.num_pages = 0
            st.session_state.num_chunks = 0
            
            # 3. Clean up the data directory (not locked)
            import shutil
            if os.path.exists("data"):
                try:
                    shutil.rmtree("data")
                except Exception:
                    pass
            os.makedirs("data", exist_ok=True)
            
            # 4. Clean up the db directory (we catch PermissionErrors in case Windows locks SQLite)
            if os.path.exists("db"):
                try:
                    shutil.rmtree("db")
                except PermissionError:
                    # Windows file lock warning workaround. 
                    # The collection is already deleted, so the database is empty.
                    pass
            os.makedirs("db", exist_ok=True)
            
            st.success("Database cleared successfully!")
            st.rerun()
        except Exception as ex:
            st.error(f"Error resetting database: {ex}")
    
    st.markdown("### 🧠 Interview Insight")
    st.warning(
        "**Why RAG?**\n\n"
        "Retrieval-Augmented Generation solves knowledge-cutoff and prevents hallucinations "
        "by feeding precise context chunks directly into the LLM prompt window, generating "
        "fully grounded medical responses with citations."
    )

# 5. Sidebar or main section for PDF upload
st.markdown('<div class="section-title">📂 1. Upload Document</div>', unsafe_allow_html=True)
uploaded_file = st.file_uploader(
    "Upload a medical PDF (e.g., clinical guidelines, research papers, reports)", 
    type=["pdf"]
)

# 6. Ingestion Pipeline
if uploaded_file is not None:
    # If the file is different from the last processed file, run the ingestion pipeline
    if st.session_state.uploaded_filename != uploaded_file.name:
        st.session_state.uploaded_filename = uploaded_file.name
        st.session_state.retriever = None  # Reset retriever for new document
        
        # Ensure the data directory exists
        os.makedirs("data", exist_ok=True)
        
        # Save file to disk
        file_path = os.path.join("data", uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
            
        # Run Ingestion
        status_text = st.empty()
        progress_bar = st.progress(0)
        
        try:
            status_text.text("Loading and extracting PDF pages...")
            progress_bar.progress(25)
            documents = load_pdf(file_path)
            st.session_state.num_pages = len(documents)
            
            status_text.text("Splitting pages into text chunks...")
            progress_bar.progress(50)
            chunks = split_documents(documents)
            st.session_state.num_chunks = len(chunks)
            
            status_text.text("Generating embeddings and building Chroma vector database...")
            progress_bar.progress(75)
            embeddings = get_embedding_model()
            vector_store = create_vector_store(chunks, embeddings, persist_directory="db")
            
            status_text.text("Initializing retriever...")
            progress_bar.progress(100)
            st.session_state.retriever = get_retriever(vector_store, k=3)
            
            status_text.empty()
            progress_bar.empty()
            st.success(f"Successfully processed and indexed '{uploaded_file.name}'!")
            
        except Exception as e:
            status_text.empty()
            progress_bar.empty()
            st.error(f"An error occurred during document ingestion: {e}")
            st.session_state.retriever = None
else:
    # If file is removed, reset state
    st.session_state.uploaded_filename = None
    st.session_state.retriever = None

# 7. Q&A Pipeline Section
st.write("---")
st.markdown('<div class="section-title">💬 2. Ask Clinical Questions</div>', unsafe_allow_html=True)

if st.session_state.retriever is not None:
    # Input field for user query
    user_query = st.text_input(
        "Enter your question based on the uploaded document:",
        placeholder="e.g. What are the diagnosis guidelines or treatments listed?"
    )
    
    if user_query:
        import time
        with st.spinner("Analyzing document and generating grounded answer..."):
            try:
                # Start timer to measure response latency
                start_time = time.time()
                
                # Run RAG
                result = run_rag_pipeline(
                    query=user_query,
                    retriever=st.session_state.retriever,
                    llm=llm
                )
                
                elapsed_time = time.time() - start_time
                
                # Display grounded answer
                st.markdown('<div class="answer-title-text">💡 Grounded Answer:</div>', unsafe_allow_html=True)
                st.markdown(
                    f'<div class="answer-box">'
                    f'{result["answer"]}'
                    f'<div style="font-size: 0.8rem; color: #718096; border-top: 1px solid #edf2f7; margin-top: 15px; padding-top: 8px; text-align: right;">'
                    f'⏱️ Response generated in {elapsed_time:.2f} seconds'
                    f'</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )
                
                # Display source references (Phase 9)
                st.markdown('<div class="section-title" style="margin-top: 15px; font-size: 1.1rem; color: #4a5568;">📚 Retrieved Source Chunks:</div>', unsafe_allow_html=True)
                
                # De-duplicate identical text content to keep the UI clean and professional
                seen_content = set()
                unique_docs = []
                for doc in result["source_documents"]:
                    cleaned_content = doc.page_content.strip()
                    if cleaned_content not in seen_content:
                        seen_content.add(cleaned_content)
                        unique_docs.append(doc)
                
                for doc in unique_docs:
                    source_name = doc.metadata.get("source", "Unknown PDF")
                    page_num = doc.metadata.get("page", 0) + 1  # 0-indexed page to 1-indexed for display
                    content = doc.page_content
                    
                    render_source_card(
                        source_name=source_name,
                        page_num=page_num,
                        content=content
                    )
                    
            except Exception as err:
                st.error(f"Error generating response: {err}")
else:
    st.info("Please upload a medical PDF above to unlock the clinical Q&A portal.")
