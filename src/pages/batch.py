"""Tab 2: Batch Analysis"""

import streamlit as st
import pandas as pd
from models import predictor
from processing import preprocess_data, aggregate_hourly, calculate_statistics
from components import section_header, data_table, line_chart, alert_box

def show():
    """Display batch analysis tab."""
    st.header("📊 Batch Analysis")
    
    section_header("Upload Dataset")
    
    uploaded_file = st.file_uploader(
        "Upload CSV file (Date, Time, EV Charging Demand columns required)",
        type="csv"
    )
    
    if uploaded_file is None:
        alert_box("Upload a CSV file to start analysis", "info")
        return
    
    try:
        df_raw = pd.read_csv(uploaded_file)
        st.success(f"✅ Loaded {len(df_raw)} records")
        
        # Preprocessing
        section_header("Data Preprocessing")
        with st.spinner("Processing data..."):
            df = preprocess_data(df_raw)
            if df is None:
                return
        
        st.success("✅ Data preprocessed")
        
        # Statistics
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
        
        # Hourly aggregation
        section_header("Hourly Analysis")
        
        df_hourly = aggregate_hourly(df)
        if df_hourly is not None:
            line_chart(
                df_hourly,
                'Datetime',
                'EV Charging Demand (kW)',
                "Hourly Demand Pattern"
            )
            
            data_table(df_hourly.head(10), "Sample Data (First 10 Hours)")
        
        # Predictions
        section_header("Batch Predictions")
        
        if predictor is None:
            alert_box("Model not loaded", "error")
            return
        
        if st.button("🔮 Generate Predictions"):
            with st.spinner("Generating predictions..."):
                try:
                    features = df[['Hour', 'DayOfWeek', 'Demand_Lag_1', 
                                   'Demand_Lag_2', 'Rolling_Avg_3h']].fillna(0)
                    
                    predictions = predictor.predict(features)
                    
                    df['Prediction'] = predictions
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric(
                            "Avg Error",
                            f"{(df['EV Charging Demand (kW)'] - df['Prediction']).abs().mean():.2f} kW"
                        )
                    
                    with col2:
                        st.metric(
                            "Max Error",
                            f"{(df['EV Charging Demand (kW)'] - df['Prediction']).abs().max():.2f} kW"
                        )
                    
                    st.success("✅ Predictions generated")
                    
                    # Download results
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="📥 Download Results (CSV)",
                        data=csv,
                        file_name="batch_predictions.csv",
                        mime="text/csv"
                    )
                    
                except Exception as e:
                    alert_box(f"Prediction error: {str(e)}", "error")
        
    except Exception as e:
        alert_box(f"File processing error: {str(e)}", "error")
