"""Tab 4: Operations Dashboard"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
from processing import format_number
from components import section_header, status_badge, bar_chart, alert_box

def show():
    """Display operations dashboard tab."""
    st.header("📈 Operations Dashboard")
    
    # System status
    section_header("System Status")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Backend Health", "🟢 Online")
        
    with col2:
        st.metric("Data Freshness", "5 min ago")
    
    with col3:
        st.metric("Model Accuracy", "94.2%")
    
    # Key metrics
    section_header("Key Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    # Generate sample data
    current_demand = np.random.uniform(60, 150)
    daily_peak = np.random.uniform(150, 250)
    active_chargers = np.random.randint(20, 80)
    efficiency = np.random.uniform(85, 99)
    
    with col1:
        demand_str = format_number(current_demand, 1)
        st.metric("Current Demand", f"{demand_str} kW")
    
    with col2:
        peak_str = format_number(daily_peak, 1)
        st.metric("Daily Peak", f"{peak_str} kW")
    
    with col3:
        st.metric("Active Chargers", active_chargers)
    
    with col4:
        eff_str = format_number(efficiency, 1)
        st.metric("Efficiency", f"{eff_str}%")
    
    # Demand pattern
    section_header("24-Hour Demand Pattern")
    
    hours = list(range(24))
    demands = [
        50 + 30 * np.sin(h * np.pi / 12) + np.random.normal(0, 5)
        for h in hours
    ]
    
    demand_data = pd.DataFrame({
        'Hour': hours,
        'Demand (kW)': demands
    })
    
    try:
        fig = px.line(
            demand_data,
            x='Hour',
            y='Demand (kW)',
            title="24-Hour Demand Forecast",
            template="plotly_dark",
            line_shape="spline"
        )
        fig.update_traces(
            line=dict(color='#0ea5e9', width=2),
            fill='tozeroy',
            fillcolor='rgba(14, 165, 233, 0.1)'
        )
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        alert_box(f"Chart error: {str(e)}", "error")
    
    # Weekly analysis
    section_header("Weekly Analysis")
    
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    daily_avg = [
        format_number(np.random.uniform(80, 140), 1)
        for _ in days
    ]
    
    weekly_data = pd.DataFrame({
        'Day': days,
        'Avg Demand (kW)': [float(d) for d in daily_avg]
    })
    
    try:
        fig = px.bar(
            weekly_data,
            x='Day',
            y='Avg Demand (kW)',
            title="Weekly Average Demand",
            template="plotly_dark"
        )
        fig.update_traces(marker=dict(color='#a855f7'))
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        alert_box(f"Chart error: {str(e)}", "error")
    
    # Alerts
    section_header("Active Alerts")
    
    alerts = [
        {"type": "warning", "message": "Peak demand approaching (>200 kW)"},
        {"type": "info", "message": "Scheduled maintenance: Station C at 2:00 AM"},
    ]
    
    if alerts:
        for alert in alerts:
            if alert['type'] == 'warning':
                st.warning(f"⚠️ {alert['message']}")
            else:
                st.info(f"ℹ️ {alert['message']}")
    else:
        st.success("✅ No active alerts")
    
    # Performance metrics
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
