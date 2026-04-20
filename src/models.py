"""Model Loading and Caching"""

import sys
from pathlib import Path
import numpy as np
import pandas as pd

# Setup path BEFORE any imports
PROJECT_ROOT = Path(__file__).parent.parent.absolute()
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Add backend path for ml module (needed for model unpickling)
BACKEND_PATH = PROJECT_ROOT / "End_sem" / "backend"
if str(BACKEND_PATH) not in sys.path:
    sys.path.insert(0, str(BACKEND_PATH))

import streamlit as st
import joblib

from src.config import MODEL_PATHS

# Cache busting version - increment when model loading changes
MODEL_CACHE_VERSION = "2.2.0"

class ModelPredictor:
    """Wrapper around the model bundle that handles feature engineering."""
    
    def __init__(self, estimator, feature_columns, defaults):
        self.estimator = estimator
        self.feature_columns = feature_columns
        self.defaults = defaults
    
    def predict(self, features_dict_or_array):
        """Predict on input features, filling missing with defaults."""
        # Handle numpy array input
        if isinstance(features_dict_or_array, np.ndarray):
            if features_dict_or_array.ndim == 1:
                features_dict_or_array = features_dict_or_array.reshape(1, -1)
            
            # If we have exactly the right number of features, use directly
            if features_dict_or_array.shape[1] == len(self.feature_columns):
                return self.estimator.predict(features_dict_or_array)
            
            # Otherwise pad with defaults
            df_input = pd.DataFrame(features_dict_or_array)
        else:
            # Handle dict input
            df_input = pd.DataFrame([features_dict_or_array] if isinstance(features_dict_or_array, dict) 
                                    else features_dict_or_array)
        
        # Ensure all required features exist with defaults
        for col in self.feature_columns:
            if col not in df_input.columns:
                df_input[col] = self.defaults.get(col, 0.0)
        
        # Select only required features in correct order
        X = df_input[self.feature_columns]
        
        # Make predictions
        return self.estimator.predict(X)

@st.cache_resource(show_spinner=False)
def load_model(_version=MODEL_CACHE_VERSION):
    """Load pre-trained model for EV demand prediction."""
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
        
        # Load model bundle
        model_bundle = joblib.load(str(found_path))
        st.success(f" Model loaded successfully")
        
        # Extract components
        estimator = model_bundle.get('estimator')
        feature_columns = model_bundle.get('feature_columns', [])
        defaults = model_bundle.get('defaults', {})
        
        if not estimator or not feature_columns:
            st.error("Invalid model bundle - missing estimator or feature columns")
            return None
        
        # Return wrapped predictor
        return ModelPredictor(estimator, feature_columns, defaults)
        
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
        st.warning(f" Agent system not available: {str(e)}")
        return None

# Initialize models on import
predictor = load_model()
agent_runner = load_agent()
