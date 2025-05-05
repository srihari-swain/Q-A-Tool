import os
os.environ["STREAMLIT_WATCHER_TYPE"] = "none"


import streamlit as st
import base64
from pathlib import Path
import os
from vectorstore import IngestUrls
from retriver import Retriever

st.set_page_config(page_title="Web Content Q&A Tool", page_icon="🔍")
api_key = st.secrets["GROQ_API_KEY"]

def add_dynamic_network_bg(logo_path=None):
    background_svg = '''
    <svg viewBox="0 0 1000 600" xmlns="http://www.w3.org/2000/svg">
      <rect width="100%" height="100%" fill="black"/>
      
      <!-- Define gradient for nodes -->
      <defs>
        <radialGradient id="nodeGlow" cx="50%" cy="50%" r="50%" fx="50%" fy="50%">
          <stop offset="0%" stop-color="white" stop-opacity="0.7"/>
          <stop offset="100%" stop-color="white" stop-opacity="0"/>
        </radialGradient>
        
        <!-- Define gradient for polygons -->
        <linearGradient id="polyGrad" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="white" stop-opacity="0.05"/>
          <stop offset="100%" stop-color="white" stop-opacity="0.15"/>
        </linearGradient>
        
        <!-- Pulse animation for nodes -->
        <animate id="pulseAnim" attributeName="r" values="3;5;3" dur="3s" repeatCount="indefinite" />
        
        <!-- Glowing effect -->
        <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
          <feGaussianBlur stdDeviation="2.5" result="coloredBlur"/>
          <feMerge>
            <feMergeNode in="coloredBlur"/>
            <feMergeNode in="SourceGraphic"/>
          </feMerge>
        </filter>
      </defs>
      
      <!-- Generate animated polygons -->
      <g>
        <polygon points="150,100 250,50 300,150 200,200" fill="url(#polyGrad)" stroke="rgba(255,255,255,0.2)" stroke-width="0.5">
          <animateTransform attributeName="transform" type="translate" values="0,0; 5,-5; 0,0" dur="15s" repeatCount="indefinite" />
          <animate attributeName="opacity" values="0.7;0.9;0.7" dur="8s" repeatCount="indefinite" />
        </polygon>
        
        <polygon points="700,150 800,120 850,220 750,250" fill="url(#polyGrad)" stroke="rgba(255,255,255,0.2)" stroke-width="0.5">
          <animateTransform attributeName="transform" type="translate" values="0,0; -8,3; 0,0" dur="12s" repeatCount="indefinite" />
          <animate attributeName="opacity" values="0.6;0.8;0.6" dur="10s" repeatCount="indefinite" />
        </polygon>
        
        <polygon points="300,400 400,350 450,450 350,500" fill="url(#polyGrad)" stroke="rgba(255,255,255,0.2)" stroke-width="0.5">
          <animateTransform attributeName="transform" type="translate" values="0,0; 6,8; 0,0" dur="18s" repeatCount="indefinite" />
          <animate attributeName="opacity" values="0.5;0.7;0.5" dur="9s" repeatCount="indefinite" />
        </polygon>
        
        <polygon points="600,350 700,300 750,400 650,450" fill="url(#polyGrad)" stroke="rgba(255,255,255,0.2)" stroke-width="0.5">
          <animateTransform attributeName="transform" type="translate" values="0,0; -4,-7; 0,0" dur="14s" repeatCount="indefinite" />
          <animate attributeName="opacity" values="0.6;0.8;0.6" dur="7s" repeatCount="indefinite" />
        </polygon>
        
        <polygon points="100,300 180,280 200,350 120,380" fill="url(#polyGrad)" stroke="rgba(255,255,255,0.2)" stroke-width="0.5">
          <animateTransform attributeName="transform" type="translate" values="0,0; 3,5; 0,0" dur="20s" repeatCount="indefinite" />
          <animate attributeName="opacity" values="0.5;0.7;0.5" dur="12s" repeatCount="indefinite" />
        </polygon>
        
        <polygon points="800,400 880,380 900,450 820,480" fill="url(#polyGrad)" stroke="rgba(255,255,255,0.2)" stroke-width="0.5">
          <animateTransform attributeName="transform" type="translate" values="0,0; -5,-3; 0,0" dur="16s" repeatCount="indefinite" />
          <animate attributeName="opacity" values="0.6;0.8;0.6" dur="11s" repeatCount="indefinite" />
        </polygon>
      </g>
      
      <!-- Node-link network -->
      <!-- Nodes with pulsing effect -->
      <g>
        <circle cx="200" cy="150" r="3" fill="white" opacity="0.8">
          <animate attributeName="r" values="2;3;2" dur="4s" repeatCount="indefinite" />
        </circle>
        <circle cx="350" cy="100" r="3" fill="white" opacity="0.8">
          <animate attributeName="r" values="3;4;3" dur="5s" repeatCount="indefinite" />
        </circle>
        <circle cx="500" cy="150" r="3" fill="white" opacity="0.8">
          <animate attributeName="r" values="2;3;2" dur="6s" repeatCount="indefinite" />
        </circle>
        <circle cx="650" cy="100" r="3" fill="white" opacity="0.8">
          <animate attributeName="r" values="2;3;2" dur="7s" repeatCount="indefinite" />
        </circle>
        <circle cx="800" cy="180" r="3" fill="white" opacity="0.8">
          <animate attributeName="r" values="2;3.5;2" dur="8s" repeatCount="indefinite" />
        </circle>
        <circle cx="120" cy="300" r="3" fill="white" opacity="0.8">
          <animate attributeName="r" values="2;3;2" dur="5s" repeatCount="indefinite" />
        </circle>
        <circle cx="250" cy="350" r="3" fill="white" opacity="0.8">
          <animate attributeName="r" values="2;3;2" dur="6s" repeatCount="indefinite" />
        </circle>
        <circle cx="400" cy="400" r="3" fill="white" opacity="0.8">
          <animate attributeName="r" values="2;3;2" dur="7s" repeatCount="indefinite" />
        </circle>
        <circle cx="550" cy="350" r="3" fill="white" opacity="0.8">
          <animate attributeName="r" values="2;3;2" dur="5s" repeatCount="indefinite" />
        </circle>
        <circle cx="700" cy="400" r="3" fill="white" opacity="0.8">
          <animate attributeName="r" values="2;3;2" dur="6s" repeatCount="indefinite" />
        </circle>
        <circle cx="850" cy="350" r="3" fill="white" opacity="0.8">
          <animate attributeName="r" values="2;3;2" dur="4s" repeatCount="indefinite" />
        </circle>
        <circle cx="900" cy="200" r="3" fill="white" opacity="0.8">
          <animate attributeName="r" values="2;3;2" dur="7s" repeatCount="indefinite" />
        </circle>
        <circle cx="100" cy="200" r="3" fill="white" opacity="0.8">
          <animate attributeName="r" values="2;3;2" dur="8s" repeatCount="indefinite" />
        </circle>
        <circle cx="300" cy="250" r="3" fill="white" opacity="0.8">
          <animate attributeName="r" values="2;3;2" dur="5s" repeatCount="indefinite" />
        </circle>
        <circle cx="500" cy="300" r="3" fill="white" opacity="0.8">
          <animate attributeName="r" values="2;3;2" dur="9s" repeatCount="indefinite" />
        </circle>
        <circle cx="700" cy="250" r="3" fill="white" opacity="0.8">
          <animate attributeName="r" values="2;3;2" dur="6s" repeatCount="indefinite" />
        </circle>
        <circle cx="450" cy="500" r="3" fill="white" opacity="0.8">
          <animate attributeName="r" values="2;3;2" dur="7s" repeatCount="indefinite" />
        </circle>
        <circle cx="600" cy="450" r="3" fill="white" opacity="0.8">
          <animate attributeName="r" values="2;3;2" dur="5s" repeatCount="indefinite" />
        </circle>
      </g>
      
      <!-- Featured nodes with dynamic glow -->
      <g>
        <circle cx="500" cy="300" r="10" fill="url(#nodeGlow)" opacity="0.6">
          <animate attributeName="r" values="8;12;8" dur="5s" repeatCount="indefinite" />
          <animate attributeName="opacity" values="0.4;0.7;0.4" dur="7s" repeatCount="indefinite" />
        </circle>
        <circle cx="350" cy="100" r="8" fill="url(#nodeGlow)" opacity="0.5">
          <animate attributeName="r" values="6;10;6" dur="8s" repeatCount="indefinite" />
          <animate attributeName="opacity" values="0.3;0.6;0.3" dur="6s" repeatCount="indefinite" />
        </circle>
        <circle cx="700" cy="400" r="8" fill="url(#nodeGlow)" opacity="0.5">
          <animate attributeName="r" values="6;11;6" dur="7s" repeatCount="indefinite" />
          <animate attributeName="opacity" values="0.3;0.5;0.3" dur="9s" repeatCount="indefinite" />
        </circle>
      </g>
      
      <!-- Lines connecting nodes with pulse animation -->
      <g>
        <line x1="200" y1="150" x2="350" y2="100" stroke="white" stroke-width="0.5" opacity="0.3">
          <animate attributeName="opacity" values="0.2;0.4;0.2" dur="7s" repeatCount="indefinite" />
        </line>
        <line x1="350" y1="100" x2="500" y2="150" stroke="white" stroke-width="0.5" opacity="0.3">
          <animate attributeName="opacity" values="0.2;0.5;0.2" dur="8s" repeatCount="indefinite" />
        </line>
        <line x1="500" y1="150" x2="650" y2="100" stroke="white" stroke-width="0.5" opacity="0.3">
          <animate attributeName="opacity" values="0.2;0.4;0.2" dur="10s" repeatCount="indefinite" />
        </line>
        <line x1="650" y1="100" x2="800" y2="180" stroke="white" stroke-width="0.5" opacity="0.3">
          <animate attributeName="opacity" values="0.2;0.4;0.2" dur="9s" repeatCount="indefinite" />
        </line>
        <line x1="120" y1="300" x2="250" y2="350" stroke="white" stroke-width="0.5" opacity="0.3">
          <animate attributeName="opacity" values="0.2;0.4;0.2" dur="6s" repeatCount="indefinite" />
        </line>
        <line x1="250" y1="350" x2="400" y2="400" stroke="white" stroke-width="0.5" opacity="0.3">
          <animate attributeName="opacity" values="0.2;0.5;0.2" dur="8s" repeatCount="indefinite" />
        </line>
        <line x1="400" y1="400" x2="550" y2="350" stroke="white" stroke-width="0.5" opacity="0.3">
          <animate attributeName="opacity" values="0.2;0.4;0.2" dur="7s" repeatCount="indefinite" />
        </line>
        <line x1="550" y1="350" x2="700" y2="400" stroke="white" stroke-width="0.5" opacity="0.3">
          <animate attributeName="opacity" values="0.2;0.5;0.2" dur="9s" repeatCount="indefinite" />
        </line>
        <line x1="700" y1="400" x2="850" y2="350" stroke="white" stroke-width="0.5" opacity="0.3">
          <animate attributeName="opacity" values="0.2;0.4;0.2" dur="7s" repeatCount="indefinite" />
        </line>
        <line x1="100" y1="200" x2="300" y2="250" stroke="white" stroke-width="0.5" opacity="0.3">
          <animate attributeName="opacity" values="0.2;0.4;0.2" dur="8s" repeatCount="indefinite" />
        </line>
        <line x1="300" y1="250" x2="500" y2="300" stroke="white" stroke-width="0.5" opacity="0.3">
          <animate attributeName="opacity" values="0.2;0.6;0.2" dur="6s" repeatCount="indefinite" />
        </line>
        <line x1="500" y1="300" x2="700" y2="250" stroke="white" stroke-width="0.5" opacity="0.3">
          <animate attributeName="opacity" values="0.2;0.5;0.2" dur="7s" repeatCount="indefinite" />
        </line>
        <line x1="700" y1="250" x2="900" y2="200" stroke="white" stroke-width="0.5" opacity="0.3">
          <animate attributeName="opacity" values="0.2;0.4;0.2" dur="9s" repeatCount="indefinite" />
        </line>
        <line x1="200" y1="150" x2="300" y2="250" stroke="white" stroke-width="0.5" opacity="0.3">
          <animate attributeName="opacity" values="0.2;0.4;0.2" dur="10s" repeatCount="indefinite" />
        </line>
        <line x1="300" y1="250" x2="400" y2="400" stroke="white" stroke-width="0.5" opacity="0.3">
          <animate attributeName="opacity" values="0.2;0.3;0.2" dur="8s" repeatCount="indefinite" />
        </line>
        <line x1="350" y1="100" x2="300" y2="250" stroke="white" stroke-width="0.5" opacity="0.3">
          <animate attributeName="opacity" values="0.2;0.5;0.2" dur="7s" repeatCount="indefinite" />
        </line>
        <line x1="500" y1="150" x2="500" y2="300" stroke="white" stroke-width="0.5" opacity="0.3">
          <animate attributeName="opacity" values="0.2;0.6;0.2" dur="9s" repeatCount="indefinite" />
        </line>
        <line x1="500" y1="300" x2="450" y2="500" stroke="white" stroke-width="0.5" opacity="0.3">
          <animate attributeName="opacity" values="0.2;0.4;0.2" dur="8s" repeatCount="indefinite" />
        </line>
        <line x1="500" y1="300" x2="600" y2="450" stroke="white" stroke-width="0.5" opacity="0.3">
          <animate attributeName="opacity" values="0.2;0.5;0.2" dur="6s" repeatCount="indefinite" />
        </line>
        <line x1="650" y1="100" x2="700" y2="250" stroke="white" stroke-width="0.5" opacity="0.3">
          <animate attributeName="opacity" values="0.2;0.4;0.2" dur="7s" repeatCount="indefinite" />
        </line>
        <line x1="700" y1="250" x2="700" y2="400" stroke="white" stroke-width="0.5" opacity="0.3">
          <animate attributeName="opacity" values="0.2;0.5;0.2" dur="9s" repeatCount="indefinite" />
        </line>
      </g>
      
      <!-- Small particles/stars with twinkling effect -->
      <g>
        <circle cx="150" cy="80" r="1" fill="white">
          <animate attributeName="opacity" values="0.2;0.6;0.2" dur="3s" repeatCount="indefinite" />
        </circle>
        <circle cx="420" cy="220" r="1" fill="white">
          <animate attributeName="opacity" values="0.2;0.7;0.2" dur="4s" repeatCount="indefinite" />
        </circle>
        <circle cx="670" cy="180" r="1" fill="white">
          <animate attributeName="opacity" values="0.2;0.5;0.2" dur="5s" repeatCount="indefinite" />
        </circle>
        <circle cx="820" cy="280" r="1" fill="white">
          <animate attributeName="opacity" values="0.2;0.6;0.2" dur="3.5s" repeatCount="indefinite" />
        </circle>
        <circle cx="180" cy="380" r="1" fill="white">
          <animate attributeName="opacity" values="0.2;0.7;0.2" dur="4.5s" repeatCount="indefinite" />
        </circle>
        <circle cx="350" cy="450" r="1" fill="white">
          <animate attributeName="opacity" values="0.2;0.5;0.2" dur="3s" repeatCount="indefinite" />
        </circle>
        <circle cx="550" cy="480" r="1" fill="white">
          <animate attributeName="opacity" values="0.2;0.6;0.2" dur="5s" repeatCount="indefinite" />
        </circle>
        <circle cx="780" cy="450" r="1" fill="white">
          <animate attributeName="opacity" values="0.2;0.7;0.2" dur="4s" repeatCount="indefinite" />
        </circle>
        <circle cx="900" cy="300" r="1" fill="white">
          <animate attributeName="opacity" values="0.2;0.5;0.2" dur="3.5s" repeatCount="indefinite" />
        </circle>
        <circle cx="50" cy="250" r="1" fill="white">
          <animate attributeName="opacity" values="0.2;0.6;0.2" dur="4.5s" repeatCount="indefinite" />
        </circle>
        <circle cx="250" cy="150" r="1" fill="white">
          <animate attributeName="opacity" values="0.2;0.7;0.2" dur="3s" repeatCount="indefinite" />
        </circle>
        <circle cx="450" cy="70" r="1" fill="white">
          <animate attributeName="opacity" values="0.2;0.5;0.2" dur="5s" repeatCount="indefinite" />
        </circle>
        <circle cx="620" cy="220" r="1" fill="white">
          <animate attributeName="opacity" values="0.2;0.6;0.2" dur="3.5s" repeatCount="indefinite" />
        </circle>
        <circle cx="750" cy="120" r="1" fill="white">
          <animate attributeName="opacity" values="0.2;0.7;0.2" dur="4s" repeatCount="indefinite" />
        </circle>
        <circle cx="850" cy="80" r="1" fill="white">
          <animate attributeName="opacity" values="0.2;0.5;0.2" dur="4.5s" repeatCount="indefinite" />
        </circle>
        <circle cx="100" cy="420" r="1" fill="white">
          <animate attributeName="opacity" values="0.2;0.6;0.2" dur="3s" repeatCount="indefinite" />
        </circle>
        <circle cx="300" cy="520" r="1" fill="white">
          <animate attributeName="opacity" values="0.2;0.7;0.2" dur="5s" repeatCount="indefinite" />
        </circle>
        <circle cx="530" cy="380" r="1" fill="white">
          <animate attributeName="opacity" values="0.2;0.5;0.2" dur="3.5s" repeatCount="indefinite" />
        </circle>
        <circle cx="650" cy="500" r="1" fill="white">
          <animate attributeName="opacity" values="0.2;0.6;0.2" dur="4s" repeatCount="indefinite" />
        </circle>
        <circle cx="800" cy="520" r="1" fill="white">
          <animate attributeName="opacity" values="0.2;0.7;0.2" dur="4.5s" repeatCount="indefinite" />
        </circle>
        <circle cx="950" cy="420" r="1" fill="white">
          <animate attributeName="opacity" values="0.2;0.5;0.2" dur="3s" repeatCount="indefinite" />
        </circle>
        <circle cx="970" cy="150" r="1" fill="white">
          <animate attributeName="opacity" values="0.2;0.6;0.2" dur="5s" repeatCount="indefinite" />
        </circle>
        <circle cx="30" cy="150" r="1" fill="white">
          <animate attributeName="opacity" values="0.2;0.7;0.2" dur="3.5s" repeatCount="indefinite" />
        </circle>
      </g>
      
      <!-- Add floating particle effect -->
      <g>
        <circle cx="250" cy="200" r="1" fill="white" opacity="0.6">
          <animate attributeName="cy" values="200;180;220;200" dur="20s" repeatCount="indefinite" />
          <animate attributeName="cx" values="250;260;240;250" dur="20s" repeatCount="indefinite" />
        </circle>
        <circle cx="480" cy="250" r="1" fill="white" opacity="0.6">
          <animate attributeName="cy" values="250;270;230;250" dur="25s" repeatCount="indefinite" />
          <animate attributeName="cx" values="480;470;490;480" dur="25s" repeatCount="indefinite" />
        </circle>
        <circle cx="650" cy="350" r="1" fill="white" opacity="0.6">
          <animate attributeName="cy" values="350;330;370;350" dur="22s" repeatCount="indefinite" />
          <animate attributeName="cx" values="650;660;640;650" dur="22s" repeatCount="indefinite" />
        </circle>
        <circle cx="150" cy="400" r="1" fill="white" opacity="0.6">
          <animate attributeName="cy" values="400;420;380;400" dur="28s" repeatCount="indefinite" />
          <animate attributeName="cx" values="150;140;160;150" dur="28s" repeatCount="indefinite" />
        </circle>
        <circle cx="800" cy="120" r="1" fill="white" opacity="0.6">
          <animate attributeName="cy" values="120;140;100;120" dur="18s" repeatCount="indefinite" />
          <animate attributeName="cx" values="800;810;790;800" dur="18s" repeatCount="indefinite" />
        </circle>
      </g>
      
      <!-- Add data flow animation on select paths -->
      <g>
        <!-- Data flow from left to right -->
        <circle r="2" fill="lightblue" opacity="0.7">
          <animate attributeName="cx" values="200;350" dur="3s" repeatCount="indefinite" />
          <animate attributeName="cy" values="150;100" dur="3s" repeatCount="indefinite" />
        </circle>
        
        <!-- Data flow from right to left -->
        <circle r="2" fill="lightblue" opacity="0.7">
          <animate attributeName="cx" values="800;650" dur="4s" repeatCount="indefinite" />
          <animate attributeName="cy" values="180;100" dur="4s" repeatCount="indefinite" />
        </circle>
        
        <!-- Data flow in central path -->
        <circle r="2" fill="lightblue" opacity="0.7">
          <animate attributeName="cx" values="500;500" dur="5s" repeatCount="indefinite" />
          <animate attributeName="cy" values="150;300" dur="5s" repeatCount="indefinite" />
        </circle>
        
        <!-- Data flow in bottom path -->
        <circle r="2" fill="lightblue" opacity="0.7">
          <animate attributeName="cx" values="400;550" dur="4s" repeatCount="indefinite" />
          <animate attributeName="cy" values="400;350" dur="4s" repeatCount="indefinite" />
        </circle>
      </g>
    </svg>
    '''
    
    b64 = base64.b64encode(background_svg.encode('utf-8')).decode('utf-8')
    
    css = f'''
    <style>
    /* Target both the main app container and all elements to ensure full coverage */
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {{
        background-image: url("data:image/svg+xml;base64,{b64}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    
    /* Force the background to cover the entire viewport */
    [data-testid="stAppViewContainer"] {{
        background-position: center top;
        min-height: 100vh;
    }}
    
    /* Style for app text to ensure visibility on dark background */
    div.stMarkdown p, div.stMarkdown h1, div.stMarkdown h2, div.stMarkdown h3, div.stMarkdown h4, div.stMarkdown h5, div.stMarkdown h6 {{
        color: white !important;
    }}
    
    /* Style for header and sidebar */
    .css-1d391kg, .css-1lcbmhc, [data-testid="stHeader"] {{
        background-color: rgba(0, 0, 0, 0.7) !important;
    }}
    
    /* Make sure the header styling doesn't override our background */
    header[data-testid="stHeader"] {{
        background-color: transparent !important;
    }}
    
    /* Text input fields */
    .stTextInput > div > div > input {{
        background-color: rgba(255, 255, 255, 0.1);
        color: white;
    }}
    
    /* Buttons */
    .stButton > button {{
        background-color: rgba(255, 255, 255, 0.2);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.5);
    }}
    
    .stButton > button:hover {{
        background-color: rgba(255, 255, 255, 0.3);
    }}
    
    /* Logo styling - UPDATED */
    .logo-container {{
        position: fixed;
        top: 53px;
        left: 20px;
        z-index: 1000;
        width: 170px;
        height: 80px;
        overflow: visible;
        padding: 5px;
        display: flex;
        align-items: center;
    }}
    
    .logo-container img {{
        width: 100%;
        height: auto;
        max-height: 100%;
        object-fit: contain;
    }}
    
    /* Create clearance at the top of the app for the logo */
    .main-content {{
        margin-top: 100px;
    }}
    </style>
    '''
    
    st.markdown(css, unsafe_allow_html=True)
    
    if logo_path:
        if os.path.exists(logo_path):
            with open(logo_path, "rb") as f:
                logo_contents = f.read()
            
            ext = Path(logo_path).suffix.lower()
            if ext in ['.jpg', '.jpeg']:
                mime = "image/jpeg"
            elif ext == '.png':
                mime = "image/png"
            elif ext == '.svg':
                mime = "image/svg+xml"
            else:
                mime = "image"
                
            logo_b64 = base64.b64encode(logo_contents).decode('utf-8')
            logo_html = f'''
            <div class="logo-container">
                <img src="data:{mime};base64,{logo_b64}" alt="Human.ai Logo">
            </div>
            '''
            st.markdown(logo_html, unsafe_allow_html=True)
        else:
            st.warning(f"Logo file not found at path: {logo_path}")


st.title("Web Content Q&A Tool")
st.markdown("Input URLs and ask questions about their content")

if 'vector_store' not in st.session_state:
    st.session_state.vector_store = None
if 'sources' not in st.session_state:
    st.session_state.sources = None
if 'urls_ingested' not in st.session_state:
    st.session_state.urls_ingested = False

st.subheader("Step 1: Input URLs")
urls_input = st.text_area("Enter URLs (one per line)",
                         placeholder="https://example.com\nhttps://another-site.com")
urls = [url.strip() for url in urls_input.split('\n') if url.strip()]

if st.button("Ingest URLs", disabled=not urls):
    with st.spinner("Ingesting and indexing content..."):
        try:
            vector_store_instance = IngestUrls()
            vector_store, sources = vector_store_instance.process(urls)
            st.session_state.vector_store = vector_store
            st.session_state.sources = sources
            st.session_state.urls_ingested = True
            st.success("Ingestion complete!")
            st.session_state.retriever = Retriever(st.session_state.vector_store, st.session_state.sources, api_key)
        except Exception as e:
            st.error(f"Error during ingestion: {e}")

st.markdown("---")
st.subheader("Step 2: Ask Questions")

if not st.session_state.urls_ingested:
    st.warning("Please ingest URLs first before asking questions.")
else:
    question = st.text_input("Enter your question", 
                            placeholder="What information can I find in these pages?")
    if st.button("Get Answer", disabled=not question):
        with st.spinner("Generating answer..."):
            try:
                
                answer = st.session_state.retriever.answer_question(question)
                st.subheader("Answer")
                st.write(answer)
            except Exception as e:
                st.error(f"Error generating answer: {e}")

def main():
   
    logo_path = "assets/logo.png"  
    
    add_dynamic_network_bg(logo_path)
    
    st.markdown("<div style='height: 50px;'></div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()