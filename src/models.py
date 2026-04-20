"""Model Loading and Caching"""

import sys
from pathlib import Path

# Setup path BEFORE any imports
PROJECT_ROOT = Path(__file__).parent.parent.absolute()
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
import joblib

from src.config import MODEL_PATHS

# Cache busting version - increment when model loading changes
MODEL_CACHE_VERSION = "2.1.0"

@st.cache_resource(show_spinner=False)
def load_model(_version=MODEL_CACHE_VERSION):
    """Load pre-trained Random Forest model for EV demand prediction."""
    try:
        found_path = None
        for path in MODEL_PATHS:
            model_path = Path(path)
            if model_path.exists():
                found_path = model_path
                st.info(f"Loading model from: {model_path}")
                break
        
        if found_path is None:
            st.error(f"Model file not found at: {[str(p) for p in MODEL_PATHS]}")
            return None
        
        # Load with explicit error handling
        model = joblib.load(str(found_path))
        st.success(f"✓ Model loaded successfully")
        return model
        
    except Exception as e:
        st.error(f"Model Loading Error: {str(e)}")
        import traceback
        st.error(f"Details: {traceback.format_exc()}")
        return None

@st.cache_resource(show_spinner=False)
def load_agent(_version=MODEL_CACHE_VERSION):
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
