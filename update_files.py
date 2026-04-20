#!/usr/bin/env python3
"""Script to update Streamlit files with proper feature engineering and remove emojis"""

import math

# ============= batch.py =============
batch_py = '''"""Tab 2: Batch Analysis"""

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

from src.models import predictor
from src.processing import preprocess_data, aggregate_hourly, calculate_statistics, format_number
from src.components import section_header, data_table, line_chart, alert_box

def calculate_cyclical_features(hour, day_of_week):
    """Calculate sin/cos encodings for hour and day of week."""
    hour_sin = math.sin(2 * math.pi * hour / 24)
    hour_cos = math.cos(2 * math.pi * hour / 24)
    dow_sin = math.sin(2 * math.pi * day_of_week / 7)
    dow_cos = math.cos(2 * math.pi * day_of_week / 7)
    return hour_sin, hour_cos, dow_sin, dow_cos

def show():
    """Display batch analysis tab."""
    st.header("Batch Analysis")
    
    section_header("Upload CSV File")
    
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.success("File loaded successfully")
            
            section_header("Data Preview")
            st.write(f"Shape: {df.shape[0]} rows x {df.shape[1]} columns")
            data_table(df.head(), "Raw Data Sample")
            
            section_header("Preprocessing")
            df = preprocess_data(df)
            st.success("Data preprocessed")
            
            section_header("Summary Statistics")
            if 'EV Charging Demand (kW)' in df.columns:
                stats = calculate_statistics(df, 'EV Charging Demand (kW)')
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Mean", f"{stats['mean']:.1f} kW")
                with col2:
                    st.metric("Max", f"{stats['max']:.1f} kW")
                with col3:
                    st.metric("Min", f"{stats['min']:.1f} kW")
                with col4:
                    st.metric("Std Dev", f"{stats['std']:.1f} kW")
            
            section_header("Hourly Analysis")
            df_hourly = aggregate_hourly(df)
            if df_hourly is not None:
                line_chart(df_hourly, 'Datetime', 'EV Charging Demand (kW)', "Hourly Demand Pattern")
                data_table(df_hourly.head(10), "Sample Data (First 10 Hours)")
            
            section_header("Batch Predictions")
            if predictor is None:
                alert_box("Model not loaded", "error")
                return
            
            if st.button("Generate Predictions"):
                with st.spinner("Generating predictions..."):
                    try:
                        # Get required features
                        required_cols = ['Hour', 'DayOfWeek', 'hour_sin', 'hour_cos', 'dow_sin', 'dow_cos', 'Demand_Lag_1', 'Demand_Lag_2']
                        
                        # Check if we have the features, if not compute them
                        if 'hour_sin' not in df.columns:
                            for idx, row in df.iterrows():
                                h_sin, h_cos, d_sin, d_cos = calculate_cyclical_features(row['Hour'], row['DayOfWeek'])
                                df.at[idx, 'hour_sin'] = h_sin
                                df.at[idx, 'hour_cos'] = h_cos
                                df.at[idx, 'dow_sin'] = d_sin
                                df.at[idx, 'dow_cos'] = d_cos
                        
                        # Fill missing values
                        for col in required_cols:
                            if col not in df.columns:
                                df[col] = 0.0
                        
                        features = df[required_cols].fillna(0)
                        predictions = predictor.predict(features)
                        df['Prediction'] = predictions
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Avg Error", f"{(df['EV Charging Demand (kW)'] - df['Prediction']).abs().mean():.2f} kW")
                        with col2:
                            st.metric("Max Error", f"{(df['EV Charging Demand (kW)'] - df['Prediction']).abs().max():.2f} kW")
                        
                        st.success("Predictions generated successfully")
                        csv = df.to_csv(index=False)
                        st.download_button(label="Download Results (CSV)", data=csv, file_name="batch_predictions.csv", mime="text/csv")
                    except Exception as e:
                        alert_box(f"Prediction error: {str(e)}", "error")
        except Exception as e:
            alert_box(f"File processing error: {str(e)}", "error")
'''

# ============= planning.py =============
planning_py = '''"""Tab 3: Agent Planning"""

import sys
from pathlib import Path

# Setup path to find src modules
PROJECT_ROOT = Path(__file__).parent.parent.parent.absolute()
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
import pandas as pd

from src.models import agent_runner
from src.components import section_header, alert_box

def show():
    """Display agent planning tab."""
    st.header("Agent Planning")
    
    if agent_runner is None:
        alert_box("Agent system not available", "warning")
        return
    
    section_header("Planning Query")
    
    col1, col2 = st.columns(2)
    
    with col1:
        location = st.text_input("Location/Station", value="Charging Station A, California")
    
    with col2:
        time_horizon = st.selectbox("Planning Horizon", ["Next 24 hours", "Next 7 days", "Next 30 days"])
    
    query = st.text_area("Planning Query", value="What are the optimal charging patterns for tomorrow?", height=100)
    
    if st.button("Generate Plan", key="planning_btn"):
        with st.spinner("Agent analyzing..."):
            try:
                context = {'location': location, 'horizon': time_horizon, 'query': query}
                result = agent_runner(context)
                
                if result:
                    st.success("Planning complete")
                    section_header("Generated Plan")
                    if isinstance(result, dict):
                        st.json(result)
                    else:
                        st.write(result)
                    
                    section_header("Key Recommendations")
                    recommendations = [
                        "Increase capacity during peak hours (3-6 PM)",
                        "Schedule maintenance during low demand (11 PM - 6 AM)",
                        "Monitor Grid load for potential bottlenecks"
                    ]
                    for rec in recommendations:
                        st.write(f"• {rec}")
                else:
                    alert_box("No plan generated", "warning")
            except Exception as e:
                alert_box(f"Agent error: {str(e)}", "error")
    
    if 'planning_history' not in st.session_state:
        st.session_state.planning_history = []
    
    section_header("Recent Plans")
    if st.session_state.planning_history:
        history_df = pd.DataFrame(st.session_state.planning_history)
        st.dataframe(history_df, use_container_width=True, hide_index=True)
    else:
        st.info("No plans generated yet")
'''

# ============= dashboard.py =============
dashboard_py = '''"""Tab 4: Operations Dashboard"""

import sys
from pathlib import Path

# Setup path to find src modules
PROJECT_ROOT = Path(__file__).parent.parent.parent.absolute()
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

from src.processing import format_number
from src.components import section_header, alert_box

def show():
    """Display operations dashboard tab."""
    st.header("Operations Dashboard")
    
    section_header("System Health")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Active Chargers", "156")
    with col2:
        st.metric("Current Load", f"{format_number(245.7, 1)} kW")
    with col3:
        uptime = 99.8
        st.metric("Uptime", f"{uptime}%")
    with col4:
        efficiency = 94.2
        eff_str = format_number(efficiency, 1)
        st.metric("Efficiency", f"{eff_str}%")
    
    section_header("24-Hour Demand Pattern")
    
    hours = list(range(24))
    demands = [50 + 30 * np.sin(h * np.pi / 12) + np.random.normal(0, 5) for h in hours]
    
    demand_data = pd.DataFrame({'Hour': hours, 'Demand (kW)': demands})
    
    try:
        fig = px.line(demand_data, x='Hour', y='Demand (kW)', title="24-Hour Demand Forecast",
                     template="plotly_dark", line_shape="spline")
        fig.update_traces(line=dict(color='#0ea5e9', width=2), fill='tozeroy', fillcolor='rgba(14, 165, 233, 0.1)')
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        alert_box(f"Chart error: {str(e)}", "error")
    
    section_header("Weekly Analysis")
    
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    daily_avg = [format_number(np.random.uniform(80, 140), 1) for _ in days]
    
    weekly_data = pd.DataFrame({'Day': days, 'Avg Demand (kW)': [float(d) for d in daily_avg]})
    
    try:
        fig = px.bar(weekly_data, x='Day', y='Avg Demand (kW)', title="Weekly Average Demand", template="plotly_dark")
        fig.update_traces(marker=dict(color='#a855f7'))
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        alert_box(f"Chart error: {str(e)}", "error")
    
    section_header("Active Alerts")
    
    alerts = [
        {"type": "warning", "message": "Peak demand approaching (>200 kW)"},
        {"type": "info", "message": "Scheduled maintenance: Station C at 2:00 AM"},
    ]
    
    if alerts:
        for alert in alerts:
            if alert['type'] == 'warning':
                st.warning(f"Warning: {alert['message']}")
            else:
                st.info(f"Info: {alert['message']}")
    else:
        st.success("No active alerts")
    
    section_header("Performance Metrics")
    
    metrics = {
        'Uptime': '99.8%',
        'Avg Response Time': format_number(125, 0) + ' ms',
        'Requests/Hour': '2,450',
        'Error Rate': '0.2%'
    }
    
    cols = st.columns(len(metrics))
    for col, (key, value) in zip(cols, metrics.items()):
        with col:
            st.metric(key, value)
'''

# Write files
try:
    with open('src/pages/batch.py', 'w') as f:
        f.write(batch_py)
    print("✓ batch.py created")
    
    with open('src/pages/planning.py', 'w') as f:
        f.write(planning_py)
    print("✓ planning.py created")
    
    with open('src/pages/dashboard.py', 'w') as f:
        f.write(dashboard_py)
    print("✓ dashboard.py created")
    
    print("\nAll files updated successfully!")
except Exception as e:
    print(f"Error: {e}")
