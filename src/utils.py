import streamlit as st

def apply_terminal_theme():
    """
    Injects custom CSS for a high-tech dark UI with animations.
    """
    st.markdown("""
        <style>
        /* Base Page Styling */
        .stApp {
            background-color: #050505;
            color: #e0e0e0;
        }

        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background-color: #0a0a0a;
            border-right: 1px solid #1f1f1f;
        }

        /* Pulsing Neon Button Animation */
        @keyframes pulse-glow {
            0% { border-color: #00f2ff; box-shadow: 0 0 5px #00f2ff; }
            50% { border-color: #00f2ff; box-shadow: 0 0 20px #00f2ff; }
            100% { border-color: #00f2ff; box-shadow: 0 0 5px #00f2ff; }
        }

        .stButton>button {
            width: 100%;
            background-color: transparent !important;
            color: #00f2ff !important;
            border: 2px solid #00f2ff !important;
            border-radius: 8px !important;
            font-family: 'Courier New', monospace !important;
            font-weight: bold !important;
            animation: pulse-glow 2s infinite;
            transition: all 0.3s ease;
        }

        .stButton>button:hover {
            background-color: #00f2ff !important;
            color: #000000 !important;
        }

        /* Terminal Text Styling */
        .terminal-text {
            color: #00ff41;
            font-family: 'Courier New', Courier, monospace;
            font-size: 0.9rem;
            padding: 5px;
        }

        /* Card Styling for metrics */
        div[data-testid="stMetricValue"] {
            color: #00f2ff !important;
            font-family: 'Courier New', monospace;
        }
        </style>
        """, unsafe_allow_html=True)

def print_terminal_log(message):
    """
    Renders a message in the Matrix-green terminal style.
    """
    st.markdown(f'<p class="terminal-text">> {message}</p>', unsafe_allow_html=True)