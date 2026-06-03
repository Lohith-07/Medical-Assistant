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
if "uploaded_filename" not in st.session_state:
    st.session_state.uploaded_filename = None
if "retriever" not in st.session_state:
    st.session_state.retriever = None
if "llm" not in st.session_state:
    st.session_state.llm = None

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

# Initialize LLM in session state if not done already
if st.session_state.llm is None:
    try:
        st.session_state.llm = get_llm()
    except Exception as e:
        st.error(f"Failed to initialize Gemini LLM: {e}")
        st.stop()

# 5. Sidebar or main section for PDF upload
st.write("### 1. Upload Document")
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
            
            status_text.text("Splitting pages into text chunks...")
            progress_bar.progress(50)
            chunks = split_documents(documents)
            
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
st.write("### 2. Ask Clinical Questions")

if st.session_state.retriever is not None:
    # Input field for user query
    user_query = st.text_input(
        "Enter your question based on the uploaded document:",
        placeholder="e.g. What are the diagnosis guidelines or treatments listed?"
    )
    
    if user_query:
        with st.spinner("Analyzing document and generating grounded answer..."):
            try:
                # Run RAG
                result = run_rag_pipeline(
                    query=user_query,
                    retriever=st.session_state.retriever,
                    llm=st.session_state.llm
                )
                
                # Display grounded answer
                st.markdown("#### Grounded Answer:")
                st.markdown(
                    f'<div class="answer-box">{result["answer"]}</div>',
                    unsafe_allow_html=True
                )
                
                # Display source references (Phase 9)
                st.markdown("#### Retrieved Source Chunks:")
                for doc in result["source_documents"]:
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
