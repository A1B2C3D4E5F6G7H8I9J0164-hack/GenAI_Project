"""Data Processing Functions"""

import pandas as pd
import numpy as np
import streamlit as st

def preprocess_data(df_raw):
    """Transform raw CSV data into model-ready features."""
    df = df_raw.copy()
    try:
        # Temporal features
        df['Datetime'] = pd.to_datetime(
            df['Date'] + ' ' + df['Time'], 
            format='mixed'
        )
        df['Hour'] = df['Datetime'].dt.hour
        df['DayOfWeek'] = df['Datetime'].dt.dayofweek
        
        # Time-series memory
        target_col = 'EV Charging Demand (kW)'
        df['Demand_Lag_1'] = df[target_col].shift(1)
        df['Demand_Lag_2'] = df[target_col].shift(2)
        df['Rolling_Avg_3h'] = df[target_col].rolling(window=3).mean().shift(1)
        
        # Fill missing values
        df = df.bfill().ffill()
        return df
        
    except Exception as e:
        st.error(f" Processing Error: {str(e)}")
        return None

def aggregate_hourly(df):
    """Aggregate data to hourly intervals."""
    try:
        df_hourly = df.set_index('Datetime').resample('H').agg({
            'EV Charging Demand (kW)': 'mean',
            'Hour': 'first',
            'DayOfWeek': 'first'
        }).reset_index()
        return df_hourly
    except Exception as e:
        st.error(f" Aggregation Error: {str(e)}")
        return None

def calculate_statistics(df, column):
    """Calculate key statistics for a column."""
    try:
        return {
            'mean': df[column].mean(),
            'std': df[column].std(),
            'min': df[column].min(),
            'max': df[column].max(),
            'median': df[column].median(),
            'q25': df[column].quantile(0.25),
            'q75': df[column].quantile(0.75),
        }
    except Exception as e:
        st.error(f" Statistics Error: {str(e)}")
        return None

def format_number(value, decimals=2):
    """Format number for display."""
    try:
        if pd.isna(value):
            return "N/A"
        return f"{float(value):.{decimals}f}"
    except:
        return "N/A"
