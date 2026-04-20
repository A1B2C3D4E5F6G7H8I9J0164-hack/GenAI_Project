"""Tab 4: Operations Dashboard"""

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
