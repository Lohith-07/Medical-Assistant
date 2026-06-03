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
        /* Import premium sans-serif typography */
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
        
        /* Apply fonts across the application */
        html, body, [class*="css"], .main, .stApp {
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            background-color: #f7fafc;
        }
        
        /* Container page structure */
        .block-container {
            padding-top: 3rem !important;
            padding-bottom: 5rem !important;
        }
        
        /* Custom Header Styling */
        .header-container {
            text-align: center;
            padding: 30px 20px;
            background: linear-gradient(135deg, #1a365d 0%, #2a4365 100%);
            border-radius: 16px;
            margin-bottom: 35px;
            box-shadow: 0 10px 15px -3px rgba(26, 54, 93, 0.15), 0 4px 6px -2px rgba(26, 54, 93, 0.05);
            color: #ffffff;
            position: relative;
            overflow: hidden;
        }
        .header-container::before {
            content: "";
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.05) 0%, transparent 60%);
            pointer-events: none;
        }
        .header-title {
            font-weight: 800;
            font-size: 2.6rem;
            margin-bottom: 8px;
            letter-spacing: -0.5px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 12px;
        }
        .header-subtitle {
            font-size: 1.1rem;
            font-weight: 400;
            color: #e2e8f0;
            max-width: 600px;
            margin: 5px auto 0 auto;
            line-height: 1.4;
        }
        
        /* Styling Streamlit inputs: File Uploader */
        div[data-testid="stFileUploader"] {
            border: 2px dashed #cbd5e0 !important;
            border-radius: 12px !important;
            padding: 15px 25px !important;
            background-color: #ffffff !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05) !important;
        }
        div[data-testid="stFileUploader"]:hover {
            border-color: #3182ce !important;
            background-color: #ebf8ff !important;
            box-shadow: 0 10px 15px -3px rgba(49, 130, 206, 0.1) !important;
        }
        
        /* Styling Streamlit inputs: Text Input Field */
        div[data-baseweb="input"] {
            border-radius: 10px !important;
            border: 1.5px solid #e2e8f0 !important;
            background-color: #ffffff !important;
            transition: all 0.2s ease-in-out !important;
            padding: 2px 5px !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.02) !important;
        }
        div[data-baseweb="input"]:focus-within {
            border-color: #3182ce !important;
            box-shadow: 0 0 0 3px rgba(49, 130, 206, 0.18) !important;
        }
        
        /* Custom section titles */
        .section-title {
            font-weight: 700;
            color: #2d3748;
            font-size: 1.25rem;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        /* Grounded Answer Card styling */
        .answer-box {
            background-color: #ffffff;
            border: 1px solid #e2e8f0;
            border-left: 5px solid #3182ce;
            padding: 22px;
            border-radius: 10px;
            color: #2d3748;
            line-height: 1.65;
            margin-top: 15px;
            margin-bottom: 30px;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.02), 0 4px 6px -2px rgba(0, 0, 0, 0.02);
            font-size: 1.05rem;
        }
        .answer-title-text {
            font-weight: 700;
            font-size: 1.15rem;
            color: #2b6cb0;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        /* Citation / Source Cards styling with lift micro-animation */
        .source-card {
            background-color: #ffffff;
            border: 1px solid #edf2f7;
            border-left: 4px solid #319795; /* Medical teal accent */
            padding: 18px;
            border-radius: 8px;
            margin-top: 15px;
            margin-bottom: 15px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.03), 0 2px 4px -1px rgba(0, 0, 0, 0.02);
            transition: all 0.3s cubic-bezier(0.165, 0.84, 0.44, 1);
        }
        .source-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 12px 20px -5px rgba(0, 0, 0, 0.08), 0 4px 6px -2px rgba(0, 0, 0, 0.04);
            border-left-color: #2c7a7b;
        }
        .source-header {
            font-weight: 700;
            color: #2c7a7b;
            font-size: 0.95rem;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 6px;
        }
        .source-content {
            font-size: 0.92rem;
            color: #4a5568;
            line-height: 1.55;
            font-style: normal;
        }
        
        /* Global override for status blocks */
        div[data-testid="stNotification"] {
            border-radius: 8px !important;
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
            <div class="header-subtitle">Analyze clinical records & guidelines securely with local vector search and grounded LLM answers</div>
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
