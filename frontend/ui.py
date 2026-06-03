import streamlit as st

def setup_page():
    """
    Sets up the Streamlit page configurations and injects custom CSS 
    for a clean, professional medical assistant theme.
    """
    st.set_page_config(
        page_title="Medical RAG Assistant",
        page_icon="🩺",
        layout="centered",
        initial_sidebar_state="collapsed"
    )
    
    # Custom CSS for modern, minimal, and premium medical-themed design
    st.markdown(
        """
        <style>
        /* Base styles */
        .main {
            font-family: 'Inter', sans-serif;
            background-color: #fdfdfd;
        }
        
        /* Custom Header Styling */
        .header-container {
            text-align: center;
            padding: 20px 0;
            border-bottom: 2px solid #eef2f5;
            margin-bottom: 30px;
        }
        .header-title {
            color: #1a365d;
            font-weight: 800;
            font-size: 2.5rem;
            margin-bottom: 0px;
        }
        .header-subtitle {
            color: #4a5568;
            font-size: 1.1rem;
            font-weight: 400;
            margin-top: 5px;
        }
        
        /* Citation Cards styling */
        .source-card {
            background-color: #ffffff;
            border-left: 4px solid #3182ce;
            padding: 15px;
            border-radius: 6px;
            margin-top: 15px;
            margin-bottom: 15px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        }
        .source-header {
            font-weight: 700;
            color: #2b6cb0;
            font-size: 0.95rem;
            margin-bottom: 5px;
        }
        .source-content {
            font-size: 0.9rem;
            color: #2d3748;
            line-height: 1.5;
        }
        
        /* Answer Box Styling */
        .answer-box {
            background-color: #ebf8ff;
            border: 1px solid #bee3f8;
            padding: 20px;
            border-radius: 8px;
            color: #2b6cb0;
            line-height: 1.6;
            margin-bottom: 25px;
        }
        .answer-title {
            font-weight: 700;
            font-size: 1.1rem;
            color: #2b6cb0;
            margin-bottom: 8px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def render_header():
    """
    Renders the app title and subtitle.
    """
    st.markdown(
        """
        <div class="header-container">
            <div class="header-title">🩺 Medical RAG Assistant</div>
            <div class="header-subtitle">Upload medical PDFs and get fully grounded answers powered by Gemini API</div>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_source_card(source_name: str, page_num: int, content: str):
    """
    Renders a styled card displaying a document chunk snippet.
    """
    # Clean up the file path to show just the file name
    file_name = source_name.split("\\")[-1].split("/")[-1]
    st.markdown(
        f"""
        <div class="source-card">
            <div class="source-header">📄 Reference: {file_name} — Page {page_num}</div>
            <div class="source-content">"{content.strip()}"</div>
        </div>
        """,
        unsafe_allow_html=True
    )
