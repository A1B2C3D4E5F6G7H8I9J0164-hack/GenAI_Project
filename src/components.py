"""Reusable UI Components"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

def metric_card(label, value, unit="", icon=""):
    """Display metric card with label and value."""
    st.metric(label=label, value=value)

def section_header(title):
    """Display section header."""
    st.markdown(f"### {title}")

def status_badge(status, label):
    """Display status badge (online/offline/alert)."""
    colors = {
        'online': '#10b981',
        'offline': '#6b7280',
        'alert': '#ff003c'
    }
    color = colors.get(status, '#ff003c')
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
            line=dict(color='#00f2ff', width=2),
            fill='tozeroy',
            fillcolor='rgba(0, 242, 255, 0.1)'
        )
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Chart Error: {str(e)}")

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
        fig.update_traces(marker=dict(color='#ff003c'))
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Chart Error: {str(e)}")

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
    st.info(f"[{type_.upper()}] {message}")

def input_section(title):
    """Create input section with header."""
    st.markdown(f"#### {title}")
