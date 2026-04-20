import streamlit as st

def apply_terminal_theme():
    """
    Professional dark theme CSS matching the React frontend design.
    Features: Glass morphism, gradients, smooth animations, modern typography.
    """
    st.markdown("""
        <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        html, body, .stApp {
            background: linear-gradient(135deg, #050505 0%, #0a0a0f 100%);
            color: #e0e0e0;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
        }

        /* Main container */
        .stApp {
            background-color: #050505;
        }

        .main {
            background: linear-gradient(135deg, #050505 0%, #0a0a0f 100%);
        }

        /* Header styling */
        .header-container {
            background: rgba(5, 5, 5, 0.8);
            border-bottom: 1px solid rgba(34, 211, 238, 0.1);
            padding: 2rem 1rem;
            margin-bottom: 2rem;
            backdrop-filter: blur(10px);
        }

        .header-title {
            font-size: 2.5rem;
            font-weight: 700;
            background: linear-gradient(135deg, #22d3ee 0%, #06b6d4 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 0.5rem;
            letter-spacing: -0.5px;
        }

        .header-subtitle {
            color: #a1a1a6;
            font-size: 0.95rem;
            font-weight: 400;
        }

        /* Card styling - Glass morphism */
        .glass-card {
            background: rgba(20, 20, 20, 0.6);
            border: 1px solid rgba(34, 211, 238, 0.15);
            border-radius: 12px;
            padding: 1.5rem;
            backdrop-filter: blur(10px);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .glass-card:hover {
            border-color: rgba(34, 211, 238, 0.3);
            box-shadow: 0 8px 32px rgba(34, 211, 238, 0.1);
            transform: translateY(-2px);
        }

        /* Gradient accent cards */
        .accent-card-cyan {
            background: rgba(34, 211, 238, 0.05);
            border: 1px solid rgba(34, 211, 238, 0.2);
        }

        .accent-card-violet {
            background: rgba(168, 85, 247, 0.05);
            border: 1px solid rgba(168, 85, 247, 0.2);
        }

        .accent-card-emerald {
            background: rgba(52, 211, 153, 0.05);
            border: 1px solid rgba(52, 211, 153, 0.2);
        }

        /* Buttons */
        .stButton > button {
            width: 100%;
            background: linear-gradient(135deg, #22d3ee 0%, #06b6d4 100%) !important;
            color: #000 !important;
            border: none !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.5px !important;
            padding: 0.75rem 1.5rem !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 15px rgba(34, 211, 238, 0.2) !important;
        }

        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 25px rgba(34, 211, 238, 0.3) !important;
        }

        .stButton > button:active {
            transform: translateY(0) !important;
        }

        /* Secondary buttons */
        .secondary-btn {
            background: transparent !important;
            color: #22d3ee !important;
            border: 1px solid #22d3ee !important;
        }

        /* Text inputs and selects */
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input,
        .stSelectbox > div > div > select,
        .stMultiSelect > div > div > select {
            background-color: rgba(20, 20, 20, 0.8) !important;
            border: 1px solid rgba(34, 211, 238, 0.2) !important;
            color: #e0e0e0 !important;
            border-radius: 6px !important;
        }

        .stTextInput > div > div > input:focus,
        .stNumberInput > div > div > input:focus,
        .stSelectbox > div > div > select:focus {
            border-color: rgba(34, 211, 238, 0.6) !important;
            box-shadow: 0 0 0 3px rgba(34, 211, 238, 0.1) !important;
        }

        /* Tabs */
        .stTabs {
            margin-top: 1.5rem;
        }

        .stTabs [data-baseweb="tab-list"] {
            border-bottom: 1px solid rgba(34, 211, 238, 0.15);
            gap: 1rem;
        }

        .stTabs [data-baseweb="tab-list"] button {
            color: #a1a1a6 !important;
            border-radius: 6px 6px 0 0 !important;
            padding: 0.75rem 1rem !important;
            font-weight: 500;
            transition: all 0.3s ease;
        }

        .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
            color: #22d3ee !important;
            border-bottom: 2px solid #22d3ee !important;
        }

        .stTabs [data-baseweb="tab-list"] button:hover {
            color: #22d3ee !important;
        }

        /* Expanders */
        .streamlit-expanderHeader {
            background: transparent !important;
            border-radius: 6px !important;
        }

        .streamlit-expanderContent {
            border: 1px solid rgba(34, 211, 238, 0.15) !important;
            border-radius: 6px !important;
            background: rgba(20, 20, 20, 0.4) !important;
        }

        /* File uploader */
        .uploadedFile {
            border: 1px solid rgba(34, 211, 238, 0.2) !important;
            border-radius: 6px !important;
            background: rgba(20, 20, 20, 0.6) !important;
        }

        /* Metrics */
        .stMetric {
            background: rgba(20, 20, 20, 0.6) !important;
            border: 1px solid rgba(34, 211, 238, 0.15) !important;
            border-radius: 8px !important;
            padding: 1rem !important;
        }

        div[data-testid="stMetricValue"] {
            color: #22d3ee !important;
            font-size: 1.8rem !important;
            font-weight: 700 !important;
        }

        div[data-testid="stMetricLabel"] {
            color: #a1a1a6 !important;
            font-size: 0.85rem !important;
            font-weight: 500 !important;
        }

        /* DataFrames */
        .stDataFrame {
            border: 1px solid rgba(34, 211, 238, 0.1) !important;
            border-radius: 6px !important;
        }

        /* Spinners and loading */
        .stSpinner > div {
            color: #22d3ee !important;
        }

        /* Alerts */
        .stSuccess {
            background: rgba(52, 211, 153, 0.1) !important;
            border: 1px solid rgba(52, 211, 153, 0.3) !important;
            border-radius: 6px !important;
        }

        .stInfo {
            background: rgba(34, 211, 238, 0.1) !important;
            border: 1px solid rgba(34, 211, 238, 0.3) !important;
            border-radius: 6px !important;
        }

        .stWarning {
            background: rgba(250, 204, 21, 0.1) !important;
            border: 1px solid rgba(250, 204, 21, 0.3) !important;
            border-radius: 6px !important;
        }

        .stError {
            background: rgba(239, 68, 68, 0.1) !important;
            border: 1px solid rgba(239, 68, 68, 0.3) !important;
            border-radius: 6px !important;
        }

        /* Terminal text */
        .terminal-text {
            color: #22d3ee;
            font-family: 'Courier New', monospace;
            font-size: 0.85rem;
            margin: 0.25rem 0;
            padding: 0.25rem 0.5rem;
            background: rgba(34, 211, 238, 0.05);
            border-left: 2px solid #22d3ee;
        }

        /* Scrollbar styling */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }

        ::-webkit-scrollbar-track {
            background: rgba(34, 211, 238, 0.05);
        }

        ::-webkit-scrollbar-thumb {
            background: rgba(34, 211, 238, 0.2);
            border-radius: 4px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: rgba(34, 211, 238, 0.4);
        }

        /* Divider */
        hr {
            border: 0;
            border-top: 1px solid rgba(34, 211, 238, 0.1);
            margin: 2rem 0;
        }

        /* Sidebar */
        .stSidebar {
            background: linear-gradient(135deg, rgba(5, 5, 5, 0.8) 0%, rgba(10, 10, 15, 0.8) 100%);
        }

        .stSidebar > div {
            border-right: 1px solid rgba(34, 211, 238, 0.1);
        }
        </style>
    """, unsafe_allow_html=True)

def print_terminal_log(message: str):
    """Display a terminal-style log message with professional styling."""
    st.markdown(f'<p class="terminal-text"> {message}</p>', unsafe_allow_html=True)