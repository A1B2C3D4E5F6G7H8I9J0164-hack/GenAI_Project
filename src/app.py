"""NEURAL GRID - EV Demand Forecasting System

Main Streamlit application entry point.
Organizes tabs for inference, batch analysis, planning, and dashboard.
"""

import sys
import os
from pathlib import Path

# Setup path to project root for imports
PROJECT_ROOT = Path(__file__).parent.parent.absolute()
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st

# Import local modules with explicit src. prefix
try:
    from src.utils import apply_terminal_theme
    from src.styles import MAIN_STYLES
    from src.config import PAGE_CONFIG
    from src.pages import inference, batch, planning, dashboard
except ImportError as e:
    st.error(f"Import Error: {e}\nMake sure all files are in src/ directory")
    st.stop()

def main():
    """Main application."""
    
    st.set_page_config(**PAGE_CONFIG)
    apply_terminal_theme()
    st.markdown(MAIN_STYLES, unsafe_allow_html=True)
    
    st.title("⚡ NEURAL GRID")
    st.write("Advanced EV Charging Network Forecasting System")
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "🔮 Inference",
        "📊 Batch Analysis",
        "🤖 Planning",
        "📈 Dashboard"
    ])
    
    with tab1:
        inference.show()
    
    with tab2:
        batch.show()
    
    with tab3:
        planning.show()
    
    with tab4:
        dashboard.show()

if __name__ == "__main__":
    main()
