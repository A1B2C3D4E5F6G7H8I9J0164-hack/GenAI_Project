"""Model Loading and Caching"""

import streamlit as st
import joblib
from pathlib import Path
from config import MODEL_PATHS

@st.cache_resource
def load_model():
    """Load pre-trained Random Forest model for EV demand prediction."""
    try:
        for path in MODEL_PATHS:
            model_path = Path(path)
            if model_path.exists():
                return joblib.load(model_path)
        
        st.warning("⚠ Model file not found - predictions unavailable")
        return None
        
    except Exception as e:
        st.error(f"❌ Model Loading Error: {str(e)}")
        return None

@st.cache_resource
def load_agent():
    """Load AI agent for planning workflows."""
    try:
        from agent.run_agent import run_planning_agent
        return run_planning_agent
    except Exception as e:
        st.warning(f"⚠ Agent system not available: {str(e)}")
        return None

# Initialize models on import
predictor = load_model()
agent_runner = load_agent()
