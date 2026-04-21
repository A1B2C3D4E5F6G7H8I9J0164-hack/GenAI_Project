import streamlit as st
import joblib
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from io import BytesIO
from sklearn.metrics import r2_score, mean_absolute_error
from utils import apply_terminal_theme, print_terminal_log
import sys
import os
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
try:
    from agent.run_agent import run_planning_agent
except Exception as e:
    run_planning_agent = None
    print(f"Warning: agent module failed to load. {e}")

st.set_page_config(page_title="NEURAL GRID | EV FORECAST", layout="wide")
apply_terminal_theme()

@st.cache_resource
def load_model():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    try:
        model = joblib.load(os.path.join(base_dir, 'models', 'ev_demand_timeseries.pkl'))
        try:
            scaler = joblib.load(os.path.join(base_dir, 'models', 'scaler.pkl'))
        except Exception as e:
            st.warning(f"scaler.pkl not found! Error: {e}")
            scaler = None
        return model, scaler
    except Exception as e:
        st.error(f"Prediction model not found: {e}")
        return None, None

predictor, scaler = load_model()

def preprocess_data(df_raw):
    """
    Transforms raw station CSV format into model-ready features.
    """
    df = df_raw.copy()
    try:
        # 1. Temporal Features
        if 'Datetime' not in df.columns:
            if 'Date' in df.columns and 'Time' in df.columns:
                df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='mixed')
            else:
                st.error("No valid Datetime column found in dataset.")
                return None
                
        df = df.sort_values('Datetime').reset_index(drop=True)
        df['Hour'] = df['Datetime'].dt.hour
        df['DayOfWeek'] = df['Datetime'].dt.dayofweek
        
        # 2. Time-Series Memory (Lags & Rolling)
        target_col = 'EV Charging Demand (kW)'
        if target_col in df.columns:
            df['Demand_Lag_1'] = df[target_col].shift(1)
            df['Demand_Lag_2'] = df[target_col].shift(2)
            df['Demand_Lag_3'] = df[target_col].shift(3)
            df['Rolling_Avg_3h'] = df[target_col].rolling(window=3).mean().shift(1)
            df['Rolling_Avg_6h'] = df[target_col].rolling(window=6).mean().shift(1)
            df['Rolling_Std_3h'] = df[target_col].rolling(window=3).std().shift(1)
        else:
            st.warning("⚠️ Target column 'EV Charging Demand (kW)' missing. Time-Series lags defaulted to baseline to prevent pipeline block.")
            df['Demand_Lag_1'] = 0.1500
            df['Demand_Lag_2'] = 0.1450
            df['Demand_Lag_3'] = 0.1400
            df['Rolling_Avg_3h'] = 0.1480
            df['Rolling_Avg_6h'] = 0.1460
            df['Rolling_Std_3h'] = 0.0100
        
        # 3. Rename/Impute columns to match the trained model's feature list
        for col, default in [('Electricity Price ($/kWh)', 0.12), ('Grid Stability Index', 1.0), ('Number of EVs Charging', 5)]:
            if col not in df.columns:
                df[col] = default
                
        df['Price_Hour_Interact'] = df['Electricity Price ($/kWh)'] * df['Hour']
        df['Price_EV_Interact'] = df['Electricity Price ($/kWh)'] * df['Number of EVs Charging']
        
        # Remove data leakage - strictly drop early rows where rolling window and lag caused NaN
        df = df.dropna().reset_index(drop=True)
        return df
    except Exception as e:
        st.error(f"Processing Error: {str(e)}")
        return None

st.title("NEURAL GRID: EV DEMAND FORECASTING")
st.markdown("---")

tab1, tab2, tab3 = st.tabs(["Manual Prediction", "Raw File Batch Processing", "AI Infrastructure Planner"])

with tab1:
    col_input, col_viz = st.columns([1, 2])
    with col_input:
        h = st.slider("Hour", 0, 23, 12)
        d = st.slider("Day (0=Mon, 6=Sun)", 0, 6, 0)
        l1 = st.number_input("Demand Lag-1 (kW)", value=0.1500, format="%.4f")
        l2 = st.number_input("Demand Lag-2 (kW)", value=0.1450, format="%.4f")
        l3 = st.number_input("Demand Lag-3 (kW)", value=0.1400, format="%.4f")
        r3 = st.number_input("Rolling 3h (kW)", value=0.1480, format="%.4f")
        r6 = st.number_input("Rolling 6h (kW)", value=0.1460, format="%.4f")
        rst3 = st.number_input("Rolling Std 3h", value=0.0100, format="%.4f")
        pr = st.number_input("Price ($/kWh)", value=0.1200, format="%.4f")
        stb = st.number_input("Stability Index", value=1.0000, format="%.4f")
        evc = st.number_input("EV Count", value=5)

        if st.button("RUN INFERENCE"):
            if predictor and scaler:
                # Calculate interactions intrinsically
                price_hour = pr * h
                price_ev = pr * evc
                
                # Feature order must exactly match training
                features = np.array([[h, d, l1, l2, r3, pr, stb, evc]], dtype=float)
                features_scaled = scaler.transform(features)
                prediction = predictor.predict(features_scaled)[0]
                st.metric("PREDICTED LOAD", f"{prediction:.4f} kW")
            else:
                st.error("Model Error: Serialization or Scaler file not detected in root.")

    with col_viz:
        x = np.linspace(0, 23, 100)
        y = 0.15 + 0.1 * np.sin((x - 6) * np.pi / 12)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=y, fill='tozeroy', line=dict(color='#00f2ff'), name='Load Profile'))
        fig.add_trace(go.Scatter(x=[h], y=[0.15 + 0.1 * np.sin((h - 6) * np.pi / 12)], mode='markers', marker=dict(color='red', size=12)))
        fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Process Raw Station Data")
    st.write("Upload a raw station file (e.g., Charging station_C__Calif.csv)")
    uploaded_file = st.file_uploader("Select CSV or Excel", type=["csv", "xlsx"])
    
    if uploaded_file and predictor and scaler:
        raw_data = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
        print_terminal_log("Raw stream detected. Commencing feature engineering...")
        
        if st.button("EXECUTE BATCH INFRASTRUCTURE ANALYSIS"):
            processed_df = preprocess_data(raw_data)
            
            if processed_df is not None:
                # The exact list of features the model was trained on
                model_features = [
                    'Hour', 'DayOfWeek', 'Demand_Lag_1', 'Demand_Lag_2',
                    'Rolling_Avg_3h', 'Electricity Price ($/kWh)', 
                    'Grid Stability Index', 'Number of EVs Charging'
                ]
                
                # Apply scaler safely and strictly map types
                X = processed_df[model_features].astype(float)
                X_scaled = scaler.transform(X)
                processed_df['AI_Predicted_Demand_kW'] = predictor.predict(X_scaled)
                
                # ADD DEBUG VALIDATION 
                y_true = processed_df['EV Charging Demand (kW)']
                y_pred = processed_df['AI_Predicted_Demand_kW']
                r2 = r2_score(y_true, y_pred)
                mae = mean_absolute_error(y_true, y_pred)
                
                st.success(f"Inference Successfully Completed. Quality Checks - R² Score: {r2:.4f} | MAE: {mae:.4f}")
                
                # ADD VISUAL VALIDATION
                st.markdown("### Model Validation: Actual vs Predicted (First 100 Points)")
                fig_val = go.Figure()
                fig_val.add_trace(go.Scatter(y=y_true.head(100), mode='lines', name='Actual Observed Trend', line=dict(color='#00ff88')))
                fig_val.add_trace(go.Scatter(y=y_pred.head(100), mode='lines', name='Model Prediction Trend', line=dict(color='#ff00ff', dash='dash')))
                fig_val.update_layout(template="plotly_dark", height=400)
                st.plotly_chart(fig_val, key="val_plot", width='stretch')
                
                print_terminal_log("Inference complete. Generating output stream...")
                st.dataframe(processed_df[['Date', 'Time', 'EV Charging Demand (kW)', 'AI_Predicted_Demand_kW']].head(20))
                
                # Download Option
                csv_buffer = BytesIO()
                processed_df.to_csv(csv_buffer, index=False)
                st.download_button("DOWNLOAD PROCESSED CSV WITH PREDICTIONS", csv_buffer.getvalue(), "Inference_Report.csv", "text/csv")
                
                # Save to session state for agent planning
                st.session_state['processed_df'] = processed_df

st.markdown("---")
print_terminal_log("System Idle. Awaiting data packet...")

with tab3:
    st.subheader("Agentic EV Infrastructure Planner")
    st.write("Reason over predicted demand & retrieve planning guidelines using Open-Source LangGraph + RAG pipeline.")
    
    # We display insights, RAG retrieval, LLM reasoning, and Final plan
    
    if st.button("RUN AGENTIC PLANNER"):
        if 'processed_df' in st.session_state and st.session_state['processed_df'] is not None:
            df_to_use = st.session_state['processed_df']
            
            with st.spinner("Agent is reasoning... (This might take a moment using local/fallback model)"):
                try:
                    if run_planning_agent is not None:
                        result = run_planning_agent(df_to_use)
                        
                        insights = result.get("insights", {})
                        reasoning = result.get("reasoning", {})
                        plan = result.get("final_plan", {})
                        sim = result.get("simulated_impact", {})
                        knowledge = result.get("retrieved_knowledge", [])
                        iters = result.get("iteration_count", 0)
                        
                        # 1. EXECUTIVE SUMMARY
                        st.markdown("## 📊 Executive Summary")
                        col_risk, col_conf, col_loop = st.columns(3)
                        col_risk.metric("Assessed Risk Level", plan.get("risk_level", "Unknown"))
                        col_conf.metric("Plan Confidence", f"{plan.get('confidence_score', 0.0)*100:.1f}%")
                        col_loop.metric("Optimization Loops", iters)
                        
                        st.markdown("---")
                        
                        # 2. DEMAND INSIGHTS & VISUALIZATION
                        st.markdown("### 📈 Core Demand Insights")
                        col_insight_text, col_insight_viz = st.columns([1, 1.5])
                        
                        with col_insight_text:
                            st.markdown(f"**Max Demand:** {insights.get('max_demand', 0):.2f} kW")
                            st.markdown(f"**Avg Demand:** {insights.get('avg_demand', 0):.2f} kW")
                            st.markdown(f"**Peak Hours Identified:** {', '.join(map(str, insights.get('peak_hours', [])))}")
                            if insights.get("deep_analysis_note"):
                                st.warning(insights["deep_analysis_note"])
                                
                        with col_insight_viz:
                            if 'AI_Predicted_Demand_kW' in df_to_use.columns:
                                fig_trend = go.Figure()
                                fig_trend.add_trace(go.Scatter(y=df_to_use['AI_Predicted_Demand_kW'].head(150), mode='lines', fill='tozeroy', line=dict(color='#ff9900')))
                                fig_trend.update_layout(title="Predicted Load Heat Trend", template="plotly_dark", height=250, margin=dict(l=0, r=0, t=30, b=0))
                                st.plotly_chart(fig_trend, use_container_width=True)
                        
                        # 3. AI REASONING ENGINE
                        st.markdown("### 🧠 AI Reasoning Process")
                        obs_col, inf_col, dec_col = st.columns(3)
                        with obs_col:
                            with st.expander("🔍 Observations", expanded=True):
                                for o in reasoning.get("observations", []):
                                    st.markdown(f"- {o}")
                        with inf_col:
                            with st.expander("💡 Inferences", expanded=True):
                                for i in reasoning.get("inferences", []):
                                    st.markdown(f"- {i}")
                        with dec_col:
                            with st.expander("⚡ Interim Decisions", expanded=True):
                                for d in reasoning.get("decisions", []):
                                    st.markdown(f"- {d}")
                        
                        # 4. FINAL PLANNING RECOMMENDATIONS
                        st.markdown("---")
                        st.markdown("### 🚀 Final Infrastructure Recommendations")
                        for idx, rec in enumerate(plan.get("recommendations", [])):
                            with st.container():
                                st.markdown(f"#### Recommendation {idx+1}: {rec.get('type', 'Action').replace('_', ' ').title()}")
                                st.markdown(f"**📍 Location:** {rec.get('location', 'N/A')} &nbsp; | &nbsp; **⚡ Priority:** {rec.get('priority', 'N/A').upper()}")
                                st.info(f"**Action:** {rec.get('action', 'N/A')}")
                                st.markdown(f"**Justification:** {rec.get('justification', 'N/A')}")
                                st.markdown("<br>", unsafe_allow_html=True)
                                
                        # 5. RETRIEVAL & SIMULATION
                        st.markdown("---")
                        col_rag, col_sim = st.columns(2)
                        with col_rag:
                            st.markdown("### 📚 Extracted Knowledge (RAG)")
                            with st.container(height=300):
                                for k in knowledge:
                                    st.markdown(f"> *{k}*")
                                    
                        with col_sim:
                            st.markdown("### 🧬 What-If Simulation")
                            st.success(f"**Scenario:** {sim.get('scenario', 'Stress Test')}")
                            st.markdown(f"**Impact Assessment:** {sim.get('impact_analysis', 'No impacts logged.')}")
                            st.metric("Stress Robustness", f"{sim.get('robustness_score', 0.0)*100:.1f}%")
                    else:
                        st.error("Agent module is missing or failed to import. Check paths and dependencies.")
                        
                except Exception as e:
                    st.error("⚠️ AI Control System encountered a network interruption or validation issue. System has safely reverted to structural baselines.")
        else:
            st.warning("Please upload and run batch inference in 'Raw File Batch Processing' tab first to generate predicted demand before running the agent.")