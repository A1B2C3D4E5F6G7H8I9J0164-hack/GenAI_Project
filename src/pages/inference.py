"""Tab 1: Real-time Inference"""

import sys
from pathlib import Path

# Setup path to find src modules
PROJECT_ROOT = Path(__file__).parent.parent.parent.absolute()
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

from src.models import predictor
from src.processing import format_number, calculate_statistics
from src.components import section_header, metric_card, line_chart, alert_box
from src.config import DEMAND_WARNING_THRESHOLD, DEMAND_ALERT_THRESHOLD

def show():
    """Display inference tab."""
    st.header("⚡ Real-time Inference")
    
    section_header("Manual Prediction")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        hour = st.number_input("Hour of Day", min_value=0, max_value=23, value=12)
    
    with col2:
        day = st.selectbox("Day of Week", ["Monday", "Tuesday", "Wednesday", 
                                            "Thursday", "Friday", "Saturday", "Sunday"])
    
    with col3:
        demand_lag = st.number_input("Previous Demand (kW)", min_value=0.0, value=100.0)
    
    if st.button("🔮 Predict", key="inference_btn"):
        with st.spinner("Generating prediction..."):
            try:
                if predictor is None:
                    alert_box("Model not loaded", "error")
                    return
                
                day_map = {"Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3,
                          "Friday": 4, "Saturday": 5, "Sunday": 6}
                day_num = day_map[day]
                
                features = np.array([[hour, day_num, demand_lag, 0, 0]])
                prediction = predictor.predict(features)[0]
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Predicted Demand", f"{format_number(prediction, 1)} kW")
                
                with col2:
                    if prediction >= DEMAND_ALERT_THRESHOLD:
                        status = "🔴 Alert"
                    elif prediction >= DEMAND_WARNING_THRESHOLD:
                        status = "🟡 Warning"
                    else:
                        status = "🟢 Normal"
                    st.metric("Status", status)
                
                with col3:
                    st.metric("Confidence", "High")
                
                section_header("24-Hour Forecast")
                hours = list(range(24))
                forecasts = []
                
                for h in hours:
                    features = np.array([[h, day_num, prediction, 0, 0]])
                    forecast = predictor.predict(features)[0]
                    forecasts.append(forecast)
                
                forecast_df = pd.DataFrame({
                    'Hour': hours,
                    'Demand (kW)': forecasts
                })
                
                line_chart(forecast_df, 'Hour', 'Demand (kW)', "24-Hour Demand Forecast")
            
            except Exception as e:
                alert_box(f"Prediction failed: {str(e)}", "error")
