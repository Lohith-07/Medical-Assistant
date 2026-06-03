import streamlit as st

def setup_page():
    """
    Sets up the Streamlit page configurations and injects custom CSS 
    for a clean, professional healthcare AI assistant theme using Inter font and modern layout.
    """
    st.set_page_config(
        page_title="Medical RAG Assistant",
        page_icon="🩺",
        layout="centered",
        initial_sidebar_state="collapsed"
    )
    
    # Custom CSS applying the requested color palette:
    # - Accent Blue: #2563eb
    # - Danger Red: #ef4444
    # - Background: #f3f4f6 (Light Gray)
    # - Cards Background: #ffffff (White)
    st.markdown(
        """
        <style>
        /* Import Inter Font */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        
        /* Injected Streamlit theme overrides to force the custom color palette */
        :root, .stApp, [data-testid="stAppViewContainer"], [data-testid="stSidebar"] {
            --background-color: #f3f4f6 !important;
            --secondary-background-color: #ffffff !important;
            --text-color: #1f2937 !important;
            --primary-color: #2563eb !important;
        }
        
        /* Force typography globally */
        html, body, .main, .stApp, p, h1, h2, h3, h4, h5, h6, label, li, small, input, textarea {
            font-family: 'Inter', sans-serif !important;
        }
        
        button {
            font-family: 'Inter', sans-serif;
        }
        
        /* Force background color on all main app viewports */
        html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"], [data-testid="stAppViewBlockContainer"], .main {
            background-color: #f3f4f6 !important;
        }
        
        /* Force global text color to dark gray */
        p, span, h1, h2, h3, h4, h5, h6, label, li, small {
            color: #1f2937 !important;
        }
        
        /* Exclude header container text from global text overrides */
        .header-container, .header-container *, .header-container p, .header-container div, .header-container h1, .header-container h2 {
            color: #ffffff !important;
        }
        .header-title, .header-title * {
            color: #ffffff !important;
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
        
        /* Custom Header Styling in Dark Slate with Blue Accent */
        .header-container {
            text-align: center;
            padding: 30px 20px;
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
            border-radius: 16px;
            margin-bottom: 35px;
            box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.2);
            color: #ffffff;
            position: relative;
            overflow: hidden;
            border-bottom: 4px solid #2563eb; /* Blue Accent line */
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
            color: #ffffff !important;
        }
        .header-subtitle {
            font-size: 1.1rem;
            font-weight: 400;
            color: #94a3b8;
            max-width: 600px;
            margin: 5px auto 0 auto;
            line-height: 1.4;
        }
        
        /* Hide native Streamlit file uploader and internal controls completely */
        div[data-testid="stFileUploader"],
        .hidden-native-controls {
            display: none !important;
        }
        
        /* Clean Document Database Card styling */
        .db-section-card {
            background: #ffffff;
            padding: 2rem;
            border-radius: 1rem;
            border: 1px solid #e5e7eb;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
            margin-bottom: 25px;
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
        }
        
        /* Dropzone area styling */
        .upload-dropzone {
            border: 2px dashed #d1d5db;
            border-radius: 0.75rem;
            padding: 2rem;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            cursor: pointer;
            transition: all 0.2s ease;
        }
        
        .upload-dropzone:hover {
            border-color: #60a5fa;
            background-color: #f9fafb;
        }
        
        .upload-dropzone.dragover {
            border-color: #3b82f6;
            background-color: #eff6ff;
            transform: scale(1.01);
            box-shadow: inset 0 2px 4px 0 rgba(0, 0, 0, 0.06);
        }
        
        .dropzone-icon {
            font-size: 3rem;
            margin-bottom: 1rem;
            transition: transform 0.2s ease;
        }
        
        .upload-dropzone:hover .dropzone-icon {
            transform: scale(1.1);
        }
        
        .dropzone-title {
            font-size: 1.125rem;
            font-weight: 600;
            color: #1f2937;
            margin-bottom: 4px;
        }
        
        .dropzone-subtitle {
            font-size: 0.875rem;
            color: #6b7280;
            margin-bottom: 1rem;
        }
        
        .dropzone-info {
            font-size: 0.75rem;
            color: #9ca3af;
        }
        
        /* Actions button row */
        .actions-row {
            display: flex;
            align-items: center;
            justify-content: flex-end;
            gap: 1rem;
            border-top: 1px solid #f3f4f6;
            padding-top: 1.5rem;
        }
        
        .btn-primary {
            background-color: #2563eb;
            color: #ffffff !important;
            padding: 0.75rem 1.5rem;
            border-radius: 0.75rem;
            font-weight: 500;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            transition: all 0.2s ease;
            box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.1), 0 2px 4px -1px rgba(37, 99, 235, 0.06);
            border: none;
        }
        
        .btn-primary:hover {
            background-color: #1d4ed8;
            transform: scale(1.02);
            box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.2), 0 4px 6px -2px rgba(37, 99, 235, 0.1);
        }
        
        .btn-danger-outline {
            background-color: transparent;
            color: #ef4444 !important;
            border: 1.5px solid #ef4444;
            padding: 0.75rem 1.5rem;
            border-radius: 0.75rem;
            font-weight: 500;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            transition: all 0.2s ease;
        }
        
        .btn-danger-outline:hover {
            background-color: #ef4444;
            color: #ffffff !important;
            box-shadow: 0 4px 6px -1px rgba(239, 68, 68, 0.1);
        }
        
        .btn-danger-outline:disabled,
        .btn-primary.disabled {
            opacity: 0.5;
            cursor: not-allowed;
            pointer-events: none;
        }
        
        /* File Card Rows */
        .file-list-container {
            display: flex;
            flex-direction: column;
            gap: 0.75rem;
            max-height: 300px;
            overflow-y: auto;
            padding-right: 4px;
        }
        
        .file-list-header {
            font-size: 0.75rem;
            font-weight: 600;
            color: #9ca3af;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        
        .file-list-grid {
            display: flex;
            flex-direction: column;
            gap: 0.75rem;
        }
        
        .file-card-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            background-color: #f9fafb;
            border: 1px solid #f3f4f6;
            border-radius: 0.75rem;
            padding: 1rem;
            transition: all 0.2s ease;
        }
        
        .file-card-row:hover {
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
        }
        
        .file-card-left {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            overflow: hidden;
        }
        
        .file-card-icon {
            font-size: 1.5rem;
            color: #3b82f6;
        }
        
        .file-card-details {
            display: flex;
            flex-direction: column;
            min-w-0;
        }
        
        .file-card-name {
            font-size: 0.875rem;
            font-weight: 600;
            color: #1f2937;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        
        .file-card-size {
            font-size: 0.75rem;
            color: #6b7280;
        }
        
        .file-card-remove-btn {
            background: transparent;
            border: none;
            color: #9ca3af;
            cursor: pointer;
            font-size: 1.125rem;
            padding: 4px;
            border-radius: 0.375rem;
            transition: all 0.2s ease;
        }
        
        .file-card-remove-btn:hover {
            color: #ef4444;
            background-color: #fee2e2;
        }
        
        .file-list-stats {
            font-size: 0.8125rem;
            color: #6b7280;
            margin-top: 4px;
        }
        
        /* Styling Streamlit inputs: Text Input Field */
        div[data-baseweb="input"] {
            border-radius: 10px !important;
            border: 1.5px solid #d1d5db !important;
            background-color: #ffffff !important;
            transition: all 0.2s ease-in-out !important;
            padding: 2px 5px !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.02) !important;
        }
        div[data-baseweb="input"]:focus-within {
            border-color: #2563eb !important; /* Blue focus border */
            box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.18) !important;
        }
        
        /* Custom section titles */
        .section-title {
            font-weight: 750;
            color: #111827;
            font-size: 1.3rem;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        /* Grounded Answer Card styling */
        .answer-box {
            background-color: #ffffff;
            border: 1px solid #e5e7eb;
            border-left: 6px solid #2563eb; /* Blue left border */
            padding: 22px;
            border-radius: 10px;
            color: #1f2937;
            line-height: 1.65;
            margin-top: 15px;
            margin-bottom: 30px;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
            font-size: 1.05rem;
        }
        .answer-title-text {
            font-weight: 750;
            font-size: 1.2rem;
            color: #111827;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        /* Citation / Source Cards styling */
        .source-card {
            background-color: #ffffff;
            border: 1px solid #e5e7eb;
            border-left: 6px solid #ef4444; /* Danger color left border */
            padding: 18px;
            border-radius: 8px;
            margin-top: 15px;
            margin-bottom: 15px;
            box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
            transition: all 0.2s ease;
        }
        .source-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.08);
        }
        .source-header {
            font-weight: 600;
            color: #ef4444; /* Danger color source titles */
            font-size: 0.95rem;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 6px;
        }
        .source-content {
            font-size: 0.92rem;
            color: #1f2937;
            line-height: 1.55;
            font-style: normal;
        }
        
        /* Global override for status blocks */
        div[data-testid="stNotification"] {
            border-radius: 8px !important;
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
