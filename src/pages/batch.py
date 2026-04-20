"""Tab 2: Batch Analysis"""

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
