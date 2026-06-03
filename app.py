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



# 3. Initialize Streamlit session state variables
if "uploaded_filenames" not in st.session_state:
    st.session_state.uploaded_filenames = []
if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = "uploader_v1"
if "retriever" not in st.session_state:
    st.session_state.retriever = None
if "num_pages" not in st.session_state:
    st.session_state.num_pages = 0
if "num_chunks" not in st.session_state:
    st.session_state.num_chunks = 0
if "embeddings" not in st.session_state:
    st.session_state.embeddings = None

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

# Initialize local embedding model once at startup and cache it
if st.session_state.embeddings is None:
    try:
        with st.spinner("Loading local semantic embedding model (once at startup)..."):
            st.session_state.embeddings = get_embedding_model()
    except Exception as e:
        st.error(f"Failed to load local embedding model: {e}")
        st.stop()

# 5. Document Ingestion Section
st.markdown('<div class="section-title">📂 Document Database</div>', unsafe_allow_html=True)

# 1. Render hidden native controls (wrapped in a hidden div)
st.markdown('<div class="hidden-native-controls">', unsafe_allow_html=True)
uploaded_files = st.file_uploader(
    "Upload medical PDFs", 
    type=["pdf"],
    accept_multiple_files=True,
    label_visibility="collapsed",
    key=st.session_state.uploader_key
)
trigger_clear = st.button("🧹 Clear DB Internal", type="primary")
st.markdown('</div>', unsafe_allow_html=True)

# 2. Handle the database clearing trigger
if trigger_clear:
    try:
        # Delete collection to release handles
        if st.session_state.retriever is not None:
            try:
                st.session_state.retriever.vectorstore.delete_collection()
            except Exception:
                pass
        
        st.session_state.uploaded_filenames = []
        st.session_state.retriever = None
        st.session_state.num_pages = 0
        st.session_state.num_chunks = 0
        
        # Rotate uploader key to force reset widget
        import time
        st.session_state.uploader_key = f"uploader_{int(time.time())}"
        
        # Clean directories
        import shutil
        if os.path.exists("data"):
            try:
                shutil.rmtree("data")
            except Exception:
                pass
        os.makedirs("data", exist_ok=True)
        
        if os.path.exists("db"):
            try:
                shutil.rmtree("db")
            except PermissionError:
                pass
        os.makedirs("db", exist_ok=True)
        
        st.success("Database cleared successfully!")
        st.rerun()
    except Exception as ex:
        st.error(f"Error resetting database: {ex}")

# 3. Compile list of active files inside the custom card
files_list_html = ""
if st.session_state.retriever is not None and st.session_state.uploaded_filenames:
    files_tags = "".join([
        f'<div class="file-tag"><span class="file-tag-icon">📄</span> {fname}</div>'
        for fname in st.session_state.uploaded_filenames
    ])
    files_list_html = f"""
    <div class="active-files-container">
        <div class="active-files-title">Active Knowledge Base:</div>
        <div class="files-tags-grid">{files_tags}</div>
        <div class="files-stats">📊 {st.session_state.num_pages} pages | {st.session_state.num_chunks} text chunks indexed</div>
    </div>
    """

# 4. Render clean unified custom card UI with inline styling and script
st.markdown(
    f"""
    <div class="db-section-card">
      <div class="db-controls-row">
        <div class="db-upload-control">
          <label for="pdf-upload" class="custom-upload-btn">
            📤 Upload Medical PDFs
          </label>
          <input
            id="pdf-upload"
            type="file"
            accept=".pdf"
            multiple
          />
          <span class="upload-info-text">
            Supports multiple PDFs up to 200MB
          </span>
        </div>
        <div class="db-action-control">
          <button id="custom-clear-btn" class="custom-clear-btn">
            🧹 Clear Database
          </button>
        </div>
      </div>
      {files_list_html}
    </div>
    
    <script>
    function setupCustomListeners() {{
        const customInput = document.getElementById('pdf-upload');
        const customClearBtn = document.getElementById('custom-clear-btn');
        
        if (customInput) {{
            customInput.removeEventListener('change', handleUploadChange);
            customInput.addEventListener('change', handleUploadChange);
        }}
        if (customClearBtn) {{
            customClearBtn.removeEventListener('click', handleClearClick);
            customClearBtn.addEventListener('click', handleClearClick);
        }}
    }}
    
    function handleUploadChange(e) {{
        const customInput = e.target;
        const nativeInput = document.querySelector('.hidden-native-controls input[type="file"]');
        if (nativeInput && customInput.files.length > 0) {{
            const dataTransfer = new DataTransfer();
            for (let i = 0; i < customInput.files.length; i++) {{
                dataTransfer.items.add(customInput.files[i]);
            }}
            nativeInput.files = dataTransfer.files;
            nativeInput.dispatchEvent(new Event('change', {{ bubbles: true }}));
        }}
    }}
    
    function handleClearClick() {{
        const nativeClearBtn = document.querySelector('.hidden-native-controls button');
        if (nativeClearBtn) {{
            nativeClearBtn.click();
        }}
    }}
    
    setupCustomListeners();
    </script>
    """,
    unsafe_allow_html=True
)

# Ingestion Pipeline
if uploaded_files:
    # Get the sorted list of current filenames
    current_filenames = sorted([f.name for f in uploaded_files])
    
    # If the set of files has changed, run the ingestion pipeline
    if st.session_state.uploaded_filenames != current_filenames:
        # Reset database and files before indexing new set
        try:
            if st.session_state.retriever is not None:
                try:
                    st.session_state.retriever.vectorstore.delete_collection()
                except Exception:
                    pass
            
            st.session_state.retriever = None
            st.session_state.num_pages = 0
            st.session_state.num_chunks = 0
            
            # Clean up the data directory
            import shutil
            if os.path.exists("data"):
                try:
                    shutil.rmtree("data")
                except Exception:
                    pass
            os.makedirs("data", exist_ok=True)
            
            # Clean up the db directory
            if os.path.exists("db"):
                try:
                    shutil.rmtree("db")
                except PermissionError:
                    pass
            os.makedirs("db", exist_ok=True)
        except Exception as ex:
            st.error(f"Error preparing database: {ex}")
            
        status_text = st.empty()
        progress_bar = st.progress(0)
        all_documents = []
        
        try:
            # 1. Save all uploaded files to disk and load them
            for idx, uploaded_file in enumerate(uploaded_files):
                status_text.text(f"Saving and loading {uploaded_file.name} ({idx+1}/{len(uploaded_files)})...")
                file_path = os.path.join("data", uploaded_file.name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # Load PDF pages
                docs = load_pdf(file_path)
                all_documents.extend(docs)
                
            progress_bar.progress(30)
            st.session_state.num_pages = len(all_documents)
            
            # 2. Split pages into text chunks
            status_text.text("Splitting pages into text chunks...")
            progress_bar.progress(60)
            chunks = split_documents(all_documents)
            st.session_state.num_chunks = len(chunks)
            
            # 3. Generate embeddings and build Chroma vector database
            status_text.text("Generating embeddings and building Chroma vector database...")
            progress_bar.progress(85)
            vector_store = create_vector_store(chunks, st.session_state.embeddings, persist_directory="db")
            
            # 4. Initialize retriever
            status_text.text("Initializing retriever...")
            progress_bar.progress(100)
            st.session_state.retriever = get_retriever(vector_store, k=3)
            
            # Update active file list
            st.session_state.uploaded_filenames = current_filenames
            
            status_text.empty()
            progress_bar.empty()
            st.success(f"Successfully processed and indexed {len(uploaded_files)} document(s)!")
            st.rerun()
            
        except Exception as e:
            status_text.empty()
            progress_bar.empty()
            st.error(f"An error occurred during document ingestion: {e}")
            st.session_state.retriever = None
            st.session_state.uploaded_filenames = []

elif st.session_state.uploaded_filenames:
    # User removed all files from the uploader
    try:
        if st.session_state.retriever is not None:
            try:
                st.session_state.retriever.vectorstore.delete_collection()
            except Exception:
                pass
        
        st.session_state.uploaded_filenames = []
        st.session_state.retriever = None
        st.session_state.num_pages = 0
        st.session_state.num_chunks = 0
        
        import shutil
        if os.path.exists("data"):
            try:
                shutil.rmtree("data")
            except Exception:
                pass
        os.makedirs("data", exist_ok=True)
        
        if os.path.exists("db"):
            try:
                shutil.rmtree("db")
            except PermissionError:
                pass
        os.makedirs("db", exist_ok=True)
        
        st.success("Database cleared successfully!")
        st.rerun()
    except Exception as ex:
        st.error(f"Error resetting database: {ex}")

# Duplicate active card removed (rendered inside the main container card)

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
