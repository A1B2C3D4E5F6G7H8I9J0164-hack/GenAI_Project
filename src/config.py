"""Application Configuration"""

import streamlit as st
from pathlib import Path
import sys
import os

# Setup paths
ROOT = Path(__file__).parent.parent
BACKEND_PATH = ROOT / 'End_sem' / 'backend'
MODELS_PATH = Path(__file__).parent / 'models'

if BACKEND_PATH.exists() and str(BACKEND_PATH) not in sys.path:
    sys.path.insert(0, str(BACKEND_PATH))

# Streamlit page config
PAGE_CONFIG = {
    'page_title': "NEURAL GRID | EV Demand Forecasting",
    'layout': "wide",
    'initial_sidebar_state': "expanded",
    'menu_items': {
        'Get Help': 'https://github.com/CosmicMagnetar/GenAI_Project',
        'Report a bug': 'https://github.com/CosmicMagnetar/GenAI_Project/issues',
        'About': "Advanced EV Charging Network Forecasting System"
    }
}

# Model paths to try
MODEL_PATHS = [
    BACKEND_PATH / 'models' / 'model_bundle.joblib',  # Actual model location
    'models/ev_demand_timeseries.pkl',
    'src/models/ev_demand_timeseries.pkl',
    MODELS_PATH / 'ev_demand_timeseries.pkl',
]

# API Configuration
API_BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:8000')
API_TIMEOUT = int(os.getenv('API_TIMEOUT', '30'))

# Model thresholds
DEMAND_WARNING_THRESHOLD = 100  # kW
DEMAND_ALERT_THRESHOLD = 150    # kW
