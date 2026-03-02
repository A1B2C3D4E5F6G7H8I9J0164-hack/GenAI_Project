import streamlit as st
import joblib
import pandas as pd
import numpy as np
import time
import plotly.graph_objects as go
from datetime import datetime
from utils import apply_terminal_theme, print_terminal_log

# Page Configuration
st.set_page_config(page_title="NEURAL GRID | EV FORECAST", layout="wide")
apply_terminal_theme()

# Model Loading Logic
@st.cache_resource
def load_model():
    try:
        # Loading your specific model file
        return joblib.load('ev_demand_timeseries.pkl')
    except Exception as e:
        st.error(f"System Error: Model file 'ev_demand_timeseries.pkl' not found.")
        return None

predictor = load_model()

# Title and Subtitle
st.title("⚡ NEURAL GRID: EV DEMAND FORECASTER")
st.markdown("---")

# Layout Columns
col_input, col_viz = st.columns([1, 2])

with col_input:
    st.subheader("Data Input Stream")
    
    # User Inputs for Prediction
    target_hour = st.slider("Target Hour (24h)", 0, 23, 12)
    day_of_week = st.selectbox("Day of Week", range(7), format_func=lambda x: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][x])
    
    # Contextual Time-Series Inputs
    st.markdown("### Lag & Rolling Features")
    lag_1 = st.number_input("Demand Lag-1 (Previous Hour kW)", value=45.0)
    rolling_avg = st.number_input("Rolling 3h Average (kW)", value=42.5)
    
    # External Factors
    st.markdown("### Environmental Factors")
    grid_price = st.slider("Electricity Price ($/kWh)", 0.1, 1.0, 0.15)
    stability = st.slider("Stability Index", 0.0, 1.0, 0.95)

    if st.button("RUN NEURAL INFERENCE"):
        with st.status("Initializing Core Engine...", expanded=True) as status:
            print_terminal_log("Connecting to ev_demand_timeseries.pkl...")
            time.sleep(0.6)
            print_terminal_log("Injecting input vector...")
            time.sleep(0.4)
            
            # Formatting features in the exact order the model expects
            # Order: [Hour, Day, Lag1, RollingAvg, Price, Stability]
            feature_vector = np.array([[target_hour, day_of_week, lag_1, rolling_avg, grid_price, stability]])
            
            if predictor:
                prediction = predictor.predict(feature_vector)[0]
                status.update(label="Inference Sequence Complete", state="complete", expanded=False)
                
                # Big Result Display
                st.markdown("### SYSTEM OUTPUT")
                st.metric(label="Predicted Charging Load", value=f"{prediction:.2f} kW")
                st.balloons()
            else:
                st.error("Critical Failure: Model Offline.")

with col_viz:
    st.subheader("Grid Load Projection")
    
    # Animated Visual: Creating a smooth curve for the UI
    x_hours = np.linspace(0, 23, 100)
    # Simulated demand curve for visualization
    y_demand = 40 + 25 * np.sin((x_hours - 6) * np.pi / 12) + np.random.normal(0, 1.5, 100)
    
    fig = go.Figure()
    
    # Base Load Area
    fig.add_trace(go.Scatter(
        x=x_hours, y=y_demand,
        fill='tozeroy',
        line=dict(color='#00f2ff', width=2),
        name='Projected Load'
    ))
    
    # Target Point Marker
    fig.add_trace(go.Scatter(
        x=[target_hour], y=[40 + 25 * np.sin((target_hour - 6) * np.pi / 12)],
        mode='markers',
        marker=dict(color='red', size=15, symbol='star'),
        name='Target Node'
    ))

    fig.update_layout(
        template="plotly_dark",
        margin=dict(l=0, r=0, t=20, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(gridcolor='#1f1f1f'),
        yaxis=dict(gridcolor='#1f1f1f')
    )
    
    st.plotly_chart(fig, use_container_width=True)
    print_terminal_log("Visualizer: Frame Buffer Updated.")

# Static Footer Log
st.markdown("---")
print_terminal_log("System Idle. Awaiting new parameter set...")