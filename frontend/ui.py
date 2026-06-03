import streamlit as st

def setup_page():
    """
    Sets up the Streamlit page configurations and injects custom CSS 
    for a clean, professional medical assistant theme using the user's color palette.
    """
    st.set_page_config(
        page_title="Medical RAG Assistant",
        page_icon="🩺",
        layout="centered",
        initial_sidebar_state="collapsed"
    )
    
    # Custom CSS applying the requested color palette:
    # - Coral Red: #FB493D
    # - Deep Slate: #282B3A
    # - Soft Ice Blue: #D7DFE2
    # - Warm Gold: #FFBF25
    st.markdown(
        """
        <style>
        /* Import premium sans-serif typography */
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
        
        /* Injected Streamlit theme overrides to force the custom color palette */
        :root, .stApp, [data-testid="stAppViewContainer"], [data-testid="stSidebar"] {
            --background-color: #D7DFE2 !important;
            --secondary-background-color: #ffffff !important;
            --text-color: #282B3A !important;
            --primary-color: #FB493D !important;
        }
        
        /* Force typography globally */
        html, body, [class*="css"], .main, .stApp, .stApp * {
            font-family: 'Plus Jakarta Sans', sans-serif !important;
        }
        
        /* Force background color on all main app viewports */
        html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"], [data-testid="stAppViewBlockContainer"], .main {
            background-color: #D7DFE2 !important;
        }
        
        /* Force global text color to Deep Slate */
        p, span, h1, h2, h3, h4, h5, h6, label, li, small {
            color: #282B3A !important;
        }
        
        /* Exclude header container text from global deep slate override */
        .header-container, .header-container *, .header-container p, .header-container div, .header-container h1, .header-container h2 {
            color: #ffffff !important;
        }
        .header-title, .header-title * {
            color: #FFBF25 !important;
        }
        
        /* Completely hide the sidebar pane and its toggle buttons */
        [data-testid="stSidebar"], [data-testid="stSidebarCollapseButton"], section[data-testid="stSidebar"] {
            display: none !important;
            width: 0px !important;
        }
        
        /* Container page structure */
        .block-container {
            padding-top: 3rem !important;
            padding-bottom: 5rem !important;
        }
        
        /* Custom Header Styling in Deep Slate with Warm Gold text */
        .header-container {
            text-align: center;
            padding: 30px 20px;
            background: linear-gradient(135deg, #282B3A 0%, #1c1e28 100%);
            border-radius: 16px;
            margin-bottom: 35px;
            box-shadow: 0 10px 20px -3px rgba(40, 43, 58, 0.25);
            color: #ffffff;
            position: relative;
            overflow: hidden;
            border-bottom: 4px solid #FFBF25; /* Gold Accent line */
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
            color: #FFBF25 !important; /* Warm Gold Header */
        }
        .header-subtitle {
            font-size: 1.1rem;
            font-weight: 400;
            color: #D7DFE2;
            max-width: 600px;
            margin: 5px auto 0 auto;
            line-height: 1.4;
        }
        
        /* Styling Streamlit inputs: File Uploader */
        div[data-testid="stFileUploader"] {
            border: 2px dashed #282B3A !important;
            border-radius: 12px !important;
            padding: 15px 25px !important;
            background-color: #ffffff !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05) !important;
        }
        div[data-testid="stFileUploader"]:hover {
            border-color: #FB493D !important; /* Coral Red focus border */
            background-color: #fff9f8 !important; /* Soft warm pink-white background */
            box-shadow: 0 10px 15px -3px rgba(251, 73, 61, 0.1) !important;
        }
        
        /* Styling Streamlit inputs: Text Input Field */
        div[data-baseweb="input"] {
            border-radius: 10px !important;
            border: 1.5px solid #282B3A !important;
            background-color: #ffffff !important;
            transition: all 0.2s ease-in-out !important;
            padding: 2px 5px !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.02) !important;
        }
        div[data-baseweb="input"]:focus-within {
            border-color: #FB493D !important; /* Coral Red focus border */
            box-shadow: 0 0 0 3px rgba(251, 73, 61, 0.18) !important;
        }
        
        /* Custom section titles */
        .section-title {
            font-weight: 800;
            color: #282B3A;
            font-size: 1.3rem;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        /* Grounded Answer Card styling with Warm Gold border */
        .answer-box {
            background-color: #ffffff;
            border: 1px solid #e2e8f0;
            border-left: 6px solid #FFBF25; /* Warm Gold left border */
            padding: 22px;
            border-radius: 10px;
            color: #282B3A;
            line-height: 1.65;
            margin-top: 15px;
            margin-bottom: 30px;
            box-shadow: 0 10px 20px -3px rgba(40, 43, 58, 0.05), 0 4px 6px -2px rgba(40, 43, 58, 0.03);
            font-size: 1.05rem;
        }
        .answer-title-text {
            font-weight: 800;
            font-size: 1.2rem;
            color: #282B3A;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        /* Citation / Source Cards styling with Coral Red border and lift micro-animation */
        .source-card {
            background-color: #ffffff;
            border: 1px solid #edf2f7;
            border-left: 6px solid #FB493D; /* Coral Red left border */
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
            border-left-color: #e53e3e; /* Darker red on hover */
        }
        .source-header {
            font-weight: 700;
            color: #FB493D; /* Coral Red source titles */
            font-size: 0.95rem;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 6px;
        }
        .source-content {
            font-size: 0.92rem;
            color: #282B3A;
            line-height: 1.55;
            font-style: normal;
        }
        
        /* Global override for status blocks */
        div[data-testid="stNotification"] {
            border-radius: 8px !important;
        }
        
        /* Sidebar styling overrides */
        [data-testid="stSidebar"] {
            background-color: #ffffff !important;
            border-right: 1.5px solid #282B3A !important;
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
