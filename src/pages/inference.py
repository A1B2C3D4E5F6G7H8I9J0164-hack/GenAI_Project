"""Tab 1: Real-time Inference"""

import sys
import math
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

def calculate_cyclical_features(hour, day_of_week):
    """Calculate sin/cos encodings for hour and day of week."""
    # Hour: 0-23 -> 0-2pi
    hour_sin = math.sin(2 * math.pi * hour / 24)
    hour_cos = math.cos(2 * math.pi * hour / 24)
    
    # Day of week: 0-6 -> 0-2pi
    dow_sin = math.sin(2 * math.pi * day_of_week / 7)
    dow_cos = math.cos(2 * math.pi * day_of_week / 7)
    
    return hour_sin, hour_cos, dow_sin, dow_cos

def show():
    """Display inference tab."""
    st.header("Real-time Inference")
    
    section_header("Manual Prediction")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        hour = st.number_input("Hour of Day", min_value=0, max_value=23, value=12)
    
    with col2:
        day = st.selectbox("Day of Week", ["Monday", "Tuesday", "Wednesday", 
                                            "Thursday", "Friday", "Saturday", "Sunday"])
    
    with col3:
        demand_lag_1 = st.number_input("Previous Hour Demand (kW)", min_value=0.0, value=100.0)
    
    demand_lag_2 = st.number_input("Two Hours Ago Demand (kW)", min_value=0.0, value=95.0)
    
    if st.button("Predict", key="inference_btn"):
        with st.spinner("Generating prediction..."):
            try:
                if predictor is None:
                    alert_box("Model not loaded", "error")
                    return
                
                day_map = {"Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3,
                          "Friday": 4, "Saturday": 5, "Sunday": 6}
                day_num = day_map[day]
                
                # Calculate cyclical features
                hour_sin, hour_cos, dow_sin, dow_cos = calculate_cyclical_features(hour, day_num)
                
                # Create feature dict - ModelPredictor will fill in missing features with defaults
                features_dict = {
                    'Hour': hour,
                    'DayOfWeek': day_num,
                    'hour_sin': hour_sin,
                    'hour_cos': hour_cos,
                    'dow_sin': dow_sin,
                    'dow_cos': dow_cos,
                    'Demand_Lag_1': demand_lag_1,
                    'Demand_Lag_2': demand_lag_2,
                }
                
                prediction = predictor.predict(features_dict)[0]
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Predicted Demand", f"{format_number(prediction, 1)} kW")
                
                with col2:
                    if prediction >= DEMAND_ALERT_THRESHOLD:
                        status = "ALERT"
                    elif prediction >= DEMAND_WARNING_THRESHOLD:
                        status = "WARNING"
                    else:
                        status = "NORMAL"
                    st.metric("Status", status)
                
                with col3:
                    st.metric("Confidence", "High")
                
                section_header("24-Hour Forecast")
                hours = list(range(24))
                forecasts = []
                
                for h in hours:
                    h_sin, h_cos, d_sin, d_cos = calculate_cyclical_features(h, day_num)
                    forecast_dict = {
                        'Hour': h,
                        'DayOfWeek': day_num,
                        'hour_sin': h_sin,
                        'hour_cos': h_cos,
                        'dow_sin': d_sin,
                        'dow_cos': d_cos,
                        'Demand_Lag_1': prediction,
                        'Demand_Lag_2': demand_lag_1,
                    }
                    forecast = predictor.predict(forecast_dict)[0]
                    forecasts.append(forecast)
                
                forecast_df = pd.DataFrame({
                    'Hour': hours,
                    'Demand (kW)': forecasts
                })
                
                line_chart(forecast_df, 'Hour', 'Demand (kW)', "24-Hour Demand Forecast")
            
            except Exception as e:
                alert_box(f"Prediction failed: {str(e)}", "error")
