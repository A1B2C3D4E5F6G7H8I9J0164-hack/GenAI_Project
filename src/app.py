"""NEURAL GRID - EV Demand Forecasting System

Main Streamlit application entry point.
Organizes tabs for inference, batch analysis, planning, and dashboard.
"""

import streamlit as st
from utils import apply_terminal_theme
from styles import MAIN_STYLES
from config import PAGE_CONFIG

# Pages imports
from pages import inference, batch, planning, dashboard

def main():
    """Main application."""
    
    # Page config
    st.set_page_config(**PAGE_CONFIG)
    
    # Apply theme and styles
    apply_terminal_theme()
    st.markdown(MAIN_STYLES, unsafe_allow_html=True)
    
    # Header
    st.title("⚡ NEURAL GRID")
    st.write("Advanced EV Charging Network Forecasting System")
    
    # Tabs
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
