import streamlit as st
import joblib
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from io import BytesIO
from pathlib import Path
import sys
import os
import json
from utils import apply_terminal_theme, print_terminal_log

# Setup path for agent imports - handle both local and deployed scenarios
_root = Path(__file__).parent.parent
_backend_path = _root / 'End_sem' / 'backend'
if _backend_path.exists() and str(_backend_path) not in sys.path:
    sys.path.insert(0, str(_backend_path))

st.set_page_config(
    page_title="NEURAL GRID | EV FORECAST",
    layout="wide",
    initial_sidebar_state="expanded",
)
apply_terminal_theme()

# ==========================================
# Cached Model & Agent Loaders
# ==========================================

@st.cache_resource
def load_model():
    try:
        # Try multiple possible paths for the model file
        possible_paths = [
            'models/ev_demand_timeseries.pkl',
            'src/models/ev_demand_timeseries.pkl',
            Path(__file__).parent / 'models' / 'ev_demand_timeseries.pkl',
        ]
        
        for path in possible_paths:
            model_path = Path(path)
            if model_path.exists():
                return joblib.load(model_path)
        
        st.warning("Warning: Model file not found.")
        return None
    except Exception as e:
        st.error(f"Model Loading Error: {str(e)}")
        return None

@st.cache_resource
def load_agent():
    try:
        from agent.run_agent import run_planning_agent
        return run_planning_agent
    except Exception as e:
        st.warning(f"Warning: Agent system not available: {str(e)}")
        return None

predictor = load_model()
agent_runner = load_agent()

# ==========================================
# Data Processing Functions
# ==========================================

def preprocess_data(df_raw):
    """
    Transforms raw station CSV format into model-ready features.
    """
    df = df_raw.copy()
    try:
        # 1. Temporal Features
        df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='mixed')
        df['Hour'] = df['Datetime'].dt.hour
        df['DayOfWeek'] = df['Datetime'].dt.dayofweek
        
        # 2. Time-Series Memory (Lags & Rolling)
        target_col = 'EV Charging Demand (kW)'
        df['Demand_Lag_1'] = df[target_col].shift(1)
        df['Demand_Lag_2'] = df[target_col].shift(2)
        df['Rolling_Avg_3h'] = df[target_col].rolling(window=3).mean().shift(1)
        
        # Use bfill() and ffill() instead of deprecated method parameter
        df = df.bfill().ffill()
        return df
    except Exception as e:
        st.error(f"Processing Error: {str(e)}")
        return None

def run_agent_workflow(processed_df):
    """Run the agentic planning pipeline on processed data."""
    if agent_runner is None:
        st.error("Agent system unavailable. Install langchain and langgraph packages.")
        return None
    
    try:
        with st.spinner("Running agent planning pipeline..."):
            result = agent_runner(processed_df)
            return result
    except Exception as e:
        st.error(f"Agent Error: {str(e)}")
        return None

# ==========================================
# UI Header & Configuration
# ==========================================

# Custom header
st.markdown("""
    <div class="header-container">
        <h1 class="header-title">NEURAL GRID</h1>
        <p class="header-subtitle">Intelligent forecasting and infrastructure planning for EV charging networks</p>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <div style="display: flex; gap: 1rem; margin-bottom: 2rem; flex-wrap: wrap;">
        <div class="glass-card accent-card-cyan" style="flex: 1; min-width: 150px;">
            <p style="color: #a1a1a6; font-size: 0.85rem; margin-bottom: 0.5rem;">Status</p>
            <p style="color: #22d3ee; font-size: 1.3rem; font-weight: 600;">Online</p>
        </div>
        <div class="glass-card accent-card-emerald" style="flex: 1; min-width: 150px;">
            <p style="color: #a1a1a6; font-size: 0.85rem; margin-bottom: 0.5rem;">Model</p>
            <p style="color: #34d399; font-size: 1.3rem; font-weight: 600;">Ready</p>
        </div>
        <div class="glass-card accent-card-violet" style="flex: 1; min-width: 150px;">
            <p style="color: #a1a1a6; font-size: 0.85rem; margin-bottom: 0.5rem;">Version</p>
            <p style="color: #a855f7; font-size: 1.3rem; font-weight: 600;">2.0.0</p>
        </div>
    </div>
""", unsafe_allow_html=True)

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "Manual Prediction",
    "Batch Analysis",
    "Agent Planning",
    "Dashboard"
])

# ==========================================
# TAB 1: Manual Prediction
# ==========================================

with tab1:
    st.markdown('<div class="glass-card" style="margin-bottom: 1.5rem;"><p style="color: #a1a1a6;">Select input parameters to generate real-time demand predictions</p></div>', unsafe_allow_html=True)
    
    col_input, col_viz = st.columns([1, 2], gap="medium")
    
    with col_input:
        st.markdown('<p style="color: #22d3ee; font-weight: 600; margin-bottom: 1rem;">Input Parameters</p>', unsafe_allow_html=True)
        
        h = st.slider("Hour of Day (0-23)", 0, 23, 12, help="Select hour for prediction")
        d = st.slider("Day of Week (0=Mon, 6=Sun)", 0, 6, 0)
        l1 = st.number_input("Demand Lag-1 (kW)", value=0.1500, format="%.4f", help="Previous hour demand")
        l2 = st.number_input("Demand Lag-2 (kW)", value=0.1450, format="%.4f", help="2 hours ago demand")
        r3 = st.number_input("Rolling 3h Average (kW)", value=0.1480, format="%.4f")
        pr = st.number_input("Grid Price ($/kWh)", value=0.1200, format="%.4f")
        stb = st.number_input("Stability Index", value=1.0000, format="%.4f", min_value=0.0, max_value=2.0)
        evc = st.number_input("Active EV Count", value=5, min_value=0, step=1)

        st.markdown("")
        if st.button("RUN INFERENCE", key="inference_btn", use_container_width=True):
            if predictor:
                features = [h, d, l1, l2, r3, pr, stb, evc]
                prediction = predictor.predict([features])[0]
                
                col_m1, col_m2 = st.columns(2)
                with col_m1:
                    st.metric("Predicted Demand", f"{prediction:.4f} kW", delta=f"{prediction*1000:.0f} W")
                with col_m2:
                    risk = "Elevated" if prediction > 0.3 else "Normal"
                    st.metric("Risk Level", risk)
            else:
                st.error("Model file not found.")

    with col_viz:
        st.markdown('<p style="color: #22d3ee; font-weight: 600; margin-bottom: 1rem;">Load Profile</p>', unsafe_allow_html=True)
        x = np.linspace(0, 23, 100)
        y = 0.15 + 0.1 * np.sin((x - 6) * np.pi / 12)
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=x, y=y, fill='tozeroy',
            line=dict(color='#22d3ee', width=3),
            fillcolor='rgba(34, 211, 238, 0.15)',
            name='Load Profile',
            hovertemplate='<b>Hour:</b> %{x:.1f}<br><b>Demand:</b> %{y:.3f} kW<extra></extra>'
        ))
        fig.add_trace(go.Scatter(
            x=[h], y=[0.15 + 0.1 * np.sin((h - 6) * np.pi / 12)],
            mode='markers',
            marker=dict(color='#f43f5e', size=14, symbol='star'),
            name='Current Hour'
        ))
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            hovermode='x unified',
            height=420,
            margin=dict(t=20, b=20, l=50, r=20),
            xaxis_title="Hour of Day",
            yaxis_title="Load (kW)"
        )
        st.plotly_chart(fig, use_container_width=True)

# ==========================================
# TAB 2: Batch Analysis
# ==========================================

with tab2:
    st.markdown('<p style="color: #a1a1a6; margin-bottom: 1rem;">Upload CSV or Excel files with charging station data for batch processing and predictions</p>', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Select CSV or Excel File",
        type=["csv", "xlsx"],
        key="batch_upload",
        help="Upload station data in CSV or Excel format"
    )
    
    if uploaded_file and predictor:
        try:
            raw_data = (
                pd.read_csv(uploaded_file)
                if uploaded_file.name.endswith('.csv')
                else pd.read_excel(uploaded_file)
            )
            
            print_terminal_log(f"Loaded {len(raw_data)} records from {uploaded_file.name}")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Records", f"{len(raw_data):,}")
            with col2:
                st.metric("Columns", len(raw_data.columns))
            with col3:
                if 'Date' in raw_data.columns:
                    st.metric("Date Range", f"{len(raw_data.iloc[:, 0].unique())} days")
            
            if st.button("PROCESS & PREDICT", key="batch_process", use_container_width=True):
                processed_df = preprocess_data(raw_data)
                
                if processed_df is not None:
                    model_features = [
                        'Hour', 'DayOfWeek', 'Demand_Lag_1', 'Demand_Lag_2',
                        'Rolling_Avg_3h', 'Electricity Price ($/kWh)',
                        'Grid Stability Index', 'Number of EVs Charging'
                    ]
                    
                    X = processed_df[model_features]
                    processed_df['AI_Predicted_Demand_kW'] = predictor.predict(X)
                    
                    print_terminal_log("Inference complete")
                    
                    # Show results
                    st.markdown('<p style="color: #22d3ee; font-weight: 600; margin-bottom: 1rem; margin-top: 1.5rem;">Results Preview</p>', unsafe_allow_html=True)
                    st.dataframe(
                        processed_df[[
                            'Date', 'Time', 'EV Charging Demand (kW)',
                            'AI_Predicted_Demand_kW'
                        ]].head(10),
                        use_container_width=True
                    )
                    
                    # Metrics
                    actual = processed_df['EV Charging Demand (kW)'].values
                    predicted = processed_df['AI_Predicted_Demand_kW'].values
                    mae = np.mean(np.abs(actual - predicted))
                    rmse = np.sqrt(np.mean((actual - predicted) ** 2))
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Mean Absolute Error", f"{mae:.4f} kW")
                    with col2:
                        st.metric("RMSE", f"{rmse:.4f} kW")
                    with col3:
                        st.metric("Records Processed", f"{len(processed_df):,}")
                    
                    # Download results
                    csv_buffer = BytesIO()
                    processed_df.to_csv(csv_buffer, index=False)
                    csv_buffer.seek(0)
                    
                    st.download_button(
                        "DOWNLOAD RESULTS (CSV)",
                        csv_buffer.getvalue(),
                        "predictions.csv",
                        "text/csv",
                        use_container_width=True
                    )
                    
                    # Visualization
                    st.markdown('<p style="color: #22d3ee; font-weight: 600; margin-bottom: 1rem; margin-top: 1.5rem;">Prediction vs Actual</p>', unsafe_allow_html=True)
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=processed_df.index,
                        y=processed_df['EV Charging Demand (kW)'],
                        name='Actual',
                        line=dict(color='#22d3ee', width=2),
                        hovertemplate='<b>Index:</b> %{x}<br><b>Actual:</b> %{y:.3f} kW<extra></extra>'
                    ))
                    fig.add_trace(go.Scatter(
                        x=processed_df.index,
                        y=processed_df['AI_Predicted_Demand_kW'],
                        name='Predicted',
                        line=dict(color='#a855f7', dash='dash', width=2),
                        hovertemplate='<b>Index:</b> %{x}<br><b>Predicted:</b> %{y:.3f} kW<extra></extra>'
                    ))
                    fig.update_layout(
                        template="plotly_dark",
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        hovermode='x unified',
                        height=420,
                        margin=dict(t=20, b=20, l=50, r=20),
                        xaxis_title="Record Index",
                        yaxis_title="Demand (kW)"
                    )
                    st.plotly_chart(fig, use_container_width=True)
        
        except Exception as e:
            st.error(f"Processing Error: {str(e)}")

# ==========================================
# TAB 3: Agent Planning
# ==========================================

with tab3:
    st.markdown('<p style="color: #a1a1a6; margin-bottom: 1rem;">Upload data to run the AI planning agent for intelligent infrastructure recommendations</p>', unsafe_allow_html=True)
    
    uploaded_file_agent = st.file_uploader(
        "Select CSV or Excel File for Agent Analysis",
        type=["csv", "xlsx"],
        key="agent_upload"
    )
    
    if uploaded_file_agent:
        try:
            raw_data = (
                pd.read_csv(uploaded_file_agent)
                if uploaded_file_agent.name.endswith('.csv')
                else pd.read_excel(uploaded_file_agent)
            )
            
            processed_df = preprocess_data(raw_data)
            
            if st.button("RUN AGENT PLANNING", key="run_agent", use_container_width=True):
                result = run_agent_workflow(processed_df)
                
                if result:
                    st.session_state.agent_result = result
                    st.success("Agent planning completed successfully!")
        
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    # Display agent results if available
    if "agent_result" in st.session_state:
        result = st.session_state.agent_result
        
        # Display reasoning
        if result.get("reasoning"):
            with st.expander("Agent Reasoning", expanded=True):
                st.markdown(f'<p style="color: #a1a1a6;">{result.get("reasoning", "")}</p>', unsafe_allow_html=True)
        
        # Insights Section
        if result.get("insights"):
            st.markdown('<p style="color: #22d3ee; font-weight: 600; margin-bottom: 1rem; margin-top: 1.5rem;">Key Insights</p>', unsafe_allow_html=True)
            for insight in result["insights"]:
                st.markdown(f'<div class="glass-card accent-card-cyan"><p>{insight}</p></div>', unsafe_allow_html=True)
        
        # Planning Section
        if result.get("final_plan"):
            plan = result["final_plan"]
            st.markdown('<p style="color: #22d3ee; font-weight: 600; margin-bottom: 1rem; margin-top: 1.5rem;">Infrastructure Plan</p>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Confidence Score", f"{plan.get('confidence_score', 0):.1%}")
            with col2:
                st.metric("Risk Level", plan.get("risk_level", "Unknown"))
            
            # Recommendations
            if plan.get("recommendations"):
                st.markdown('<p style="color: #22d3ee; font-weight: 600; margin-bottom: 1rem; margin-top: 1rem;">Recommendations</p>', unsafe_allow_html=True)
                for i, rec in enumerate(plan["recommendations"], 1):
                    priority_color = "#f43f5e" if rec.get('priority') == 'high' else "#facc15" if rec.get('priority') == 'medium' else "#34d399"
                    with st.expander(f"**{rec.get('action', 'Action')}** — Priority: {rec.get('priority', 'medium').upper()}"):
                        st.markdown(f'<p style="color: #a1a1a6;"><b>Location:</b> {rec.get("location", "N/A")}</p>', unsafe_allow_html=True)
                        if rec.get('estimated_cost'):
                            st.markdown(f'<p style="color: #a1a1a6;"><b>Est. Cost:</b> ${rec.get("estimated_cost"):,.0f}</p>', unsafe_allow_html=True)
                        if rec.get('implementation_timeline'):
                            st.markdown(f'<p style="color: #a1a1a6;"><b>Timeline:</b> {rec.get("implementation_timeline")}</p>', unsafe_allow_html=True)
        
        # Simulation Results
        if result.get("simulated_impact"):
            impact = result["simulated_impact"]
            st.markdown('<p style="color: #22d3ee; font-weight: 600; margin-bottom: 1rem; margin-top: 1.5rem;">Simulation Results</p>', unsafe_allow_html=True)
            st.markdown(f'<div class="glass-card accent-card-violet"><p><b>Scenario:</b> {impact.get("scenario", "")}<br><b>Impact:</b> {impact.get("impact_analysis", "")}</p></div>', unsafe_allow_html=True)
            st.metric("Robustness Score", f"{impact.get('robustness_score', 0):.1%}")
        
        # Full State JSON (Advanced)
        if st.checkbox("Show Full Agent State (Advanced)"):
            st.json(result)

# ==========================================
# TAB 4: Dashboard
# ==========================================

with tab4:
    st.markdown('<p style="color: #a1a1a6; margin-bottom: 1rem;">Real-time monitoring and analytics dashboard for EV charging infrastructure</p>', unsafe_allow_html=True)
    
    # System status cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
            <div class="glass-card accent-card-cyan" style="text-align: center; padding: 1.5rem;">
                <p style="color: #a1a1a6; font-size: 0.85rem; margin-bottom: 0.5rem;">Active Chargers</p>
                <p style="color: #22d3ee; font-size: 2rem; font-weight: 700;">150</p>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
            <div class="glass-card accent-card-violet" style="text-align: center; padding: 1.5rem;">
                <p style="color: #a1a1a6; font-size: 0.85rem; margin-bottom: 0.5rem;">Utilization</p>
                <p style="color: #a855f7; font-size: 2rem; font-weight: 700;">72%</p>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
            <div class="glass-card accent-card-emerald" style="text-align: center; padding: 1.5rem;">
                <p style="color: #a1a1a6; font-size: 0.85rem; margin-bottom: 0.5rem;">Grid Health</p>
                <p style="color: #34d399; font-size: 2rem; font-weight: 700;">95%</p>
            </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
            <div class="glass-card accent-card-cyan" style="text-align: center; padding: 1.5rem;">
                <p style="color: #a1a1a6; font-size: 0.85rem; margin-bottom: 0.5rem;">Network Load</p>
                <p style="color: #22d3ee; font-size: 2rem; font-weight: 700;">58%</p>
            </div>
        """, unsafe_allow_html=True)
    
    # Synthetic data for demo
    hours = list(range(24))
    demand = [10 + 8 * (1 + 0.5 * ((h - 12) ** 2 / 144)) + (2 if h % 2 == 0 else -1) for h in hours]
    
    col1, col2 = st.columns([2, 1], gap="medium")
    
    with col1:
        st.markdown('<p style="color: #22d3ee; font-weight: 600; margin-bottom: 1rem; margin-top: 1.5rem;">Hourly Demand Profile</p>', unsafe_allow_html=True)
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=hours, y=demand,
            marker=dict(
                color=demand,
                colorscale='Turbo',
                line=dict(width=0)
            ),
            name='Demand (kW)',
            hovertemplate='<b>Hour:</b> %{x}:00<br><b>Demand:</b> %{y:.1f} kW<extra></extra>'
        ))
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=320,
            margin=dict(t=20, b=20, l=50, r=20),
            xaxis_title="Hour of Day",
            yaxis_title="Load (kW)",
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown('<p style="color: #22d3ee; font-weight: 600; margin-bottom: 1rem; margin-top: 1.5rem;">Quick Stats</p>', unsafe_allow_html=True)
        st.markdown(f"""
            <div class="glass-card" style="padding: 1rem;">
                <p style="color: #a1a1a6; font-size: 0.85rem; margin-bottom: 0.5rem;">Peak Hour</p>
                <p style="color: #f43f5e; font-size: 1.5rem; font-weight: 600; margin-bottom: 1rem;">14:00</p>
                
                <p style="color: #a1a1a6; font-size: 0.85rem; margin-bottom: 0.5rem;">Peak Load</p>
                <p style="color: #f43f5e; font-size: 1.5rem; font-weight: 600; margin-bottom: 1rem;">{max(demand):.1f} kW</p>
                
                <p style="color: #a1a1a6; font-size: 0.85rem; margin-bottom: 0.5rem;">Avg Load</p>
                <p style="color: #34d399; font-size: 1.5rem; font-weight: 600;">{np.mean(demand):.1f} kW</p>
            </div>
        """, unsafe_allow_html=True)
    
    # Day of week analysis
    st.markdown('<p style="color: #22d3ee; font-weight: 600; margin-bottom: 1rem; margin-top: 1.5rem;">Weekly Pattern</p>', unsafe_allow_html=True)
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    day_demand = [85.2, 87.5, 88.1, 86.9, 89.2, 72.3, 68.9]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=days, y=day_demand,
        mode='lines+markers',
        line=dict(color='#22d3ee', width=3),
        marker=dict(size=10, color='#a855f7'),
        fill='tozeroy',
        fillcolor='rgba(34, 211, 238, 0.1)',
        name='Avg Demand (kW)',
        hovertemplate='<b>%{x}</b><br><b>Demand:</b> %{y:.1f} kW<extra></extra>'
    ))
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=350,
        margin=dict(t=20, b=20, l=50, r=20),
        xaxis_title="Day of Week",
        yaxis_title="Avg Load (kW)",
        hovermode='x unified'
    )
    st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
print_terminal_log("System ready. Awaiting user action...")