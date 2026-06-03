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
        
        /* Force typography globally on standard text containers, avoiding icon font overrides */
        html, body, .main, .stApp, p, h1, h2, h3, h4, h5, h6, label, li, small, input, textarea {
            font-family: 'Plus Jakarta Sans', sans-serif !important;
        }
        
        /* Force typography on buttons without !important to prevent inheritance overrides on icons */
        button {
            font-family: 'Plus Jakarta Sans', sans-serif;
        }
        
        /* Restore font family for Streamlit's Material Icons/Symbols to prevent text rendering */
        [data-testid="stIconMaterial"], 
        [class*="Icon"], 
        [class*="icon"], 
        .material-icons, 
        i, 
        span[class*="icon"], 
        span[class*="Icon"] {
            font-family: 'Material Symbols Rounded', 'Material Symbols Outlined', 'Material Icons' !important;
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
        /* Hide native Streamlit file uploader and internal controls completely */
        div[data-testid="stFileUploader"],
        .hidden-native-controls {
            display: none !important;
        }
        
        /* Premium Document Database Card styling */
        .db-section-card {
            background: #ffffff;
            padding: 24px;
            border-radius: 16px;
            border-left: 6px solid #FFBF25; /* Gold Accent line */
            box-shadow: 0 10px 25px -5px rgba(40, 43, 58, 0.05), 0 8px 10px -6px rgba(40, 43, 58, 0.03);
            margin-bottom: 25px;
            display: flex;
            flex-direction: column;
            gap: 20px;
        }
        
        .db-controls-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 16px;
        }
        
        .db-upload-control {
            display: flex;
            align-items: center;
            gap: 16px;
            flex-wrap: wrap;
        }
        
        .custom-upload-btn {
            background: #282B3A;
            color: #ffffff !important;
            padding: 12px 24px;
            border-radius: 10px;
            cursor: pointer;
            font-size: 15px;
            font-weight: 600;
            border: none;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            transition: all 0.2s ease-in-out;
            box-shadow: 0 4px 6px rgba(40, 43, 58, 0.15);
        }
        
        .custom-upload-btn:hover {
            background: #FB493D; /* Coral Red hover */
            transform: translateY(-1px);
            box-shadow: 0 6px 12px rgba(251, 73, 61, 0.2);
        }
        
        .upload-info-text {
            color: #718096;
            font-size: 14px;
        }
        
        #pdf-upload {
            display: none !important;
        }
        
        .custom-clear-btn {
            background: transparent;
            color: #FB493D !important;
            border: 1.5px solid #FB493D;
            padding: 10px 20px;
            border-radius: 10px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 600;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
            transition: all 0.2s ease-in-out;
        }
        
        .custom-clear-btn:hover {
            background: #FB493D;
            color: #ffffff !important;
            box-shadow: 0 4px 10px rgba(251, 73, 61, 0.15);
        }
        
        /* Active file tags styling */
        .active-files-container {
            border-top: 1px solid #edf2f7;
            padding-top: 18px;
        }
        
        .active-files-title {
            font-weight: 700;
            font-size: 13px;
            color: #718096;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 10px;
        }
        
        .files-tags-grid {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-bottom: 8px;
        }
        
        .file-tag {
            background: #f7fafc;
            border: 1px solid #e2e8f0;
            color: #282B3A;
            padding: 6px 12px;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 500;
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }
        
        .file-tag-icon {
            font-size: 15px;
        }
        
        .files-stats {
            font-size: 13px;
            color: #718096;
            margin-top: 4px;
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
        <script>
        // Global listener to bridge custom HTML upload button to hidden native Streamlit uploader
        if (typeof window.customUploaderListenerSetup === 'undefined') {
            window.customUploaderListenerSetup = true;
            document.addEventListener('change', (e) => {
                if (e.target && e.target.id === 'pdf-upload') {
                    const customInput = e.target;
                    const nativeInput = document.querySelector('[data-testid="stFileUploader"] input[type="file"]');
                    if (nativeInput) {
                        const dataTransfer = new DataTransfer();
                        for (let i = 0; i < customInput.files.length; i++) {
                            dataTransfer.items.add(customInput.files[i]);
                        }
                        nativeInput.files = dataTransfer.files;
                        nativeInput.dispatchEvent(new Event('change', { bubbles: true }));
                    }
                }
            });
        }
        </script>
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
