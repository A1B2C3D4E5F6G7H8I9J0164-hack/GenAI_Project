"""Reusable UI Components"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

def metric_card(label, value, unit="", icon="📊"):
    """Display metric card with label and value."""
    col1, col2 = st.columns([3, 1])
    with col1:
        st.metric(label=label, value=value)
    with col2:
        st.write(icon)

def section_header(title):
    """Display section header."""
    st.markdown(f"### {title}")

def status_badge(status, label):
    """Display status badge (online/offline/alert)."""
    colors = {
        'online': '#10b981',
        'offline': '#6b7280',
        'alert': '#f43f5e'
    }
    color = colors.get(status, '#0ea5e9')
    html = f"""
    <div style="display: inline-block; padding: 0.35rem 0.85rem; 
                border-radius: 20px; font-size: 0.85rem; font-weight: 600; 
                background: {color}20; color: {color}; border: 1px solid {color};">
        {label}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def line_chart(data, x_col, y_col, title=""):
    """Create interactive line chart."""
    try:
        fig = px.line(
            data, 
            x=x_col, 
            y=y_col,
            title=title,
            labels={x_col: "Time", y_col: "Demand (kW)"},
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
        st.error(f"❌ Chart Error: {str(e)}")

def bar_chart(data, x_col, y_col, title=""):
    """Create interactive bar chart."""
    try:
        fig = px.bar(
            data,
            x=x_col,
            y=y_col,
            title=title,
            template="plotly_dark"
        )
        fig.update_traces(marker=dict(color='#a855f7'))
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"❌ Chart Error: {str(e)}")

def data_table(df, title=""):
    """Display formatted data table."""
    if title:
        st.write(f"**{title}**")
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=False
    )

def alert_box(message, type_="info"):
    """Display alert message."""
    icons = {
        'info': 'ℹ️',
        'success': '✅',
        'warning': '⚠️',
        'error': '❌'
    }
    icon = icons.get(type_, 'ℹ️')
    st.info(f"{icon} {message}")

def input_section(title):
    """Create input section with header."""
    st.markdown(f"#### {title}")
