"""Tab 1: Real-time Inference"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from models import predictor
from processing import format_number, calculate_statistics
from components import section_header, metric_card, line_chart, alert_box
from config import DEMAND_WARNING_THRESHOLD, DEMAND_ALERT_THRESHOLD

def show():
    """Display inference tab."""
    st.header("⚡ Real-time Inference")
    
    section_header("Manual Prediction")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        hour = st.number_input(
            "Hour of Day",
            min_value=0,
            max_value=23,
            value=datetime.now().hour
        )
    
    with col2:
        day_of_week = st.selectbox(
            "Day of Week",
            ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
            index=datetime.now().weekday()
        )
    
    with col3:
        demand_lag = st.number_input(
            "Previous Demand (kW)",
            min_value=0.0,
            max_value=500.0,
            value=75.0
        )
    
    if st.button("🔮 Predict Demand", key="predict_btn"):
        if predictor is None:
            alert_box("Model not loaded. Please try again.", "error")
            return
        
        try:
            day_num = datetime.strptime(day_of_week, "%A").weekday()
            
            features = np.array([
                [hour, day_num, demand_lag, 0, 0]
            ])
            
            prediction = predictor.predict(features)[0]
            
            st.success(f"✅ Predicted Demand: **{format_number(prediction, 2)} kW**")
            
            # Status indicator
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Prediction", f"{format_number(prediction, 1)} kW")
            with col2:
                status = "🟢 Normal"
                if prediction >= DEMAND_ALERT_THRESHOLD:
                    status = "🔴 Alert"
                elif prediction >= DEMAND_WARNING_THRESHOLD:
                    status = "🟡 Warning"
                st.metric("Status", status)
            with col3:
                st.metric("Confidence", "High")
            
            # Forecast chart
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
