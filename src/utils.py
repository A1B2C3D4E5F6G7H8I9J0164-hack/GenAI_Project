import streamlit as st

def apply_terminal_theme():
    """
    Injects professional CSS for an advanced data-driven interface.
    """
    st.markdown("""
        <style>
        .stApp {
            background-color: #050505;
            color: #e0e0e0;
            font-family: 'Courier New', monospace;
        }

        /* Pulsing Inference Button */
        @keyframes pulse-glow {
            0% { border-color: #00f2ff; box-shadow: 0 0 5px #00f2ff; }
            50% { border-color: #00f2ff; box-shadow: 0 0 15px #00f2ff; }
            100% { border-color: #00f2ff; box-shadow: 0 0 5px #00f2ff; }
        }

        .stButton>button {
            width: 100%;
            background-color: transparent !important;
            color: #00f2ff !important;
            border: 1px solid #00f2ff !important;
            border-radius: 4px !important;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 1px;
            animation: pulse-glow 3s infinite;
        }

        /* Terminal Logging */
        .terminal-text {
            color: #00ff41;
            font-family: 'Courier New', monospace;
            font-size: 0.8rem;
            margin: 0;
            padding: 2px 0;
        }

        /* Metric and Dataframe Aesthetics */
        div[data-testid="stMetricValue"] {
            color: #00f2ff !important;
        }
        
        .stDataFrame {
            border: 1px solid #1f1f1f;
        }

        div[data-testid="stFileUploader"] {
            border: 1px dashed #00f2ff;
            background-color: #0a0a0a;
            padding: 15px;
        }
        </style>
        """, unsafe_allow_html=True)

def print_terminal_log(message):
    st.markdown(f'<p class="terminal-text">[SYSTEM]: {message}</p>', unsafe_allow_html=True)