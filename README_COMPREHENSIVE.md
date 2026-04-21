# NEURAL GRID: Advanced EV Demand Forecasting System

## Project Overview

**NEURAL GRID** is an intelligent AI-powered system for predicting Electric Vehicle (EV) charging demand at grid stations using advanced machine learning, time-series analysis, and multi-agent AI planning.

The system combines:
- **Predictive Models**: WeightedEnsemble estimators with HistGradientBoosting and GradientBoosting regressors
- **Temporal Intelligence**: Cyclical time encoding for hour and day-of-week patterns
- **Feature Engineering**: 25-feature comprehensive analysis including demand lags, rolling statistics, external data
- **AI Planning**: Multi-agent architecture for infrastructure optimization
- **Interactive UI**: Streamlit-based real-time inference and batch processing

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Architecture](#architecture)
3. [Features](#features)
4. [Installation](#installation)
5. [Usage](#usage)
6. [Data Formats](#data-formats)
7. [Model Details](#model-details)
8. [Troubleshooting](#troubleshooting)
9. [Project Structure](#project-structure)
10. [Contributing](#contributing)

---

## Quick Start

### Option 1: Local Development

```bash
# Clone the repository
git clone https://github.com/CosmicMagnetar/GenAI_Project.git
cd GenAI_Project

# Install dependencies
pip install -r src/requirements.txt

# Run the Streamlit app
streamlit run src/app.py
```

### Option 2: Docker Deployment

```bash
# Build and run with Docker
docker build -t neural-grid .
docker run -p 8501:8501 neural-grid
```

### Option 3: Cloud Deployment (Render)

The app is deployed on Render and accessible at:
- **Live URL**: [Your Render app URL]
- Auto-deploys on every GitHub push to `main` branch

---

## Architecture

### System Components

```
GenAI_Project/
├── src/                          # Streamlit application
│   ├── app.py                   # Main application entry point
│   ├── utils.py                 # Utility functions
│   └── requirements.txt          # Python dependencies
│
├── End_sem/
│   ├── backend/                 # ML backend
│   │   ├── models/              # Pre-trained models
│   │   │   └── model_bundle.joblib  # Main prediction model
│   │   ├── ml/                  # Machine learning pipeline
│   │   │   ├── dataset.py       # Data loading
│   │   │   ├── preprocessor.py  # Feature engineering
│   │   │   ├── predictor.py     # Prediction wrapper
│   │   │   └── train.py         # Model training
│   │   ├── agent/               # AI planning agents
│   │   │   ├── run_agent.py     # Agent execution
│   │   │   ├── graph.py         # Workflow graph
│   │   │   └── nodes/           # Processing nodes
│   │   └── data/                # Training datasets
│   │
│   └── frontend/                # React web interface
│       └── src/                 # React components
│
├── data/                        # Sample charging station data
│   ├── Charging station_A_Calif.csv
│   ├── Charging station_B_Calif.csv
│   └── Charging station_C_Calif.csv
│
└── notebooks/                   # Jupyter notebooks for exploration
```

### System Architecture Diagram

![System Architecture](docs/architecture/system_architecture.png)

**Description**: Multi-layered architecture showing:
- User Interface Layer (Streamlit, React, Dashboard)
- Feature Engineering Layer (temporal, lags, rolling stats, interactions)
- 25-Dimensional Feature Vector Layer
- ML Model Layer (HistGradientBoosting + GradientBoosting Ensemble)
- Prediction Output (EV Charging Demand in kW)

### Data Pipeline Diagram

![Data Pipeline Flow](docs/architecture/data_pipeline.png)

**Flow**: Raw CSV Data → Merging → Feature Engineering → 25-Feature Vector → StandardScaler → Ensemble Model → EV Demand Prediction

### Model Architecture Diagram

![Model Architecture](docs/architecture/model_architecture.png)

**Components**:
- **Input**: 25 features (Temporal, Time-Series, External, Infrastructure)
- **Preprocessing**: StandardScaler normalization
- **Model**: WeightedEnsemble combining:
  - HistGradientBoostingRegressor (60% weight)
  - GradientBoostingRegressor (40% weight)
- **Output**: EV Charging Demand (kW)
- **Performance**: R² Score 0.5256, MAE 0.0706 kW

### Inference Flow

![Inference Flow](docs/architecture/inference_flow.png)

**Input Types**:
- **Manual**: Hour (0-23), DayOfWeek, demand history
- **Batch**: CSV file with hourly data
- **API**: JSON payload with features

**Process**:
1. Feature Validation & Auto-filling (missing features filled with defaults)
2. StandardScaler Transform (same as training)
3. Ensemble Prediction (60% HistGradientBoosting + 40% GradientBoosting)
4. Weighted Average (0.6 × pred1 + 0.4 × pred2)
5. Output: EV Charging Demand (kW)

---

## Image Reference Guide

Store AI-generated architecture diagrams in the `docs/architecture/` folder:

```
docs/
└── architecture/
    ├── system_architecture.png       # System components and layers
    ├── data_pipeline.png             # Data flow from raw to prediction
    ├── model_architecture.png        # ML model structure and components
    └── inference_flow.png            # Prediction inference pipeline
```

**How to add images**:
1. Generate diagrams using AI image generator (DALL-E, Midjourney, etc.)
2. Create `docs/architecture/` folder if not exists
3. Save PNG images to the folder
4. Images will automatically display in this README when rendered on GitHub

---

## Features

### 1. Real-time Inference
- Manual single-point predictions
- Interactive input sliders for Hour, Day, and historical demand
- 24-hour forecast visualization
- Demand status indicators (Normal/Warning/Alert)

### 2. Batch Processing
- Upload CSV files with EV charging data
- Automatic preprocessing and feature engineering
- Bulk predictions with error metrics (R², MAE)
- CSV download of predictions
- Data quality metrics and visualization

### 3. AI Infrastructure Planning
- Multi-agent AI system using LangChain
- Analyzes optimal charging patterns
- Recommends maintenance windows
- Grid load optimization strategies
- Real-time planning context

### 4. Operations Dashboard
- System health metrics
- 24-hour demand patterns
- Weekly analysis charts
- Active alerts and notifications
- Performance statistics

### 5. Intelligent Feature Engineering
The system automatically computes:

| Feature | Description | Type |
|---------|-------------|------|
| Hour | Hour of day (0-23) | Temporal |
| DayOfWeek | Day of week (0-6) | Temporal |
| hour_sin, hour_cos | Cyclical hour encoding | Derived |
| dow_sin, dow_cos | Cyclical day encoding | Derived |
| Demand_Lag_1/2/3 | Previous hour demands | Time-series |
| Rolling_Avg_3h/6h | 3h, 6h moving averages | Statistics |
| Rolling_Std_3h | 3h rolling std dev | Statistics |
| Electricity Price | $/kWh | External |
| Grid Stability Index | Grid health (0-1) | External |
| Number of EVs Charging | EV count | External |
| Price_Hour_Interact | Price × Hour | Interaction |
| Price_EV_Interact | Price × EV Count | Interaction |
| Solar/Wind Production | Renewable energy (kW) | External |
| Charging Station Capacity | Max capacity (kW) | Infrastructure |
| Peak Demand | Historical peak (kW) | Historical |
| Renewable Energy Usage (%) | Grid composition (%) | External |
| EV Charging Efficiency (%) | Charger efficiency (%) | Infrastructure |
| Battery Storage (kWh) | Energy storage (kWh) | Infrastructure |

---

## Installation

### Prerequisites

- **Python 3.9+** (tested on 3.12, 3.13)
- **pip** or **conda** package manager
- **Git** for version control
- 2GB RAM minimum
- 500MB disk space for model and dependencies

### Step 1: Clone Repository

```bash
git clone https://github.com/CosmicMagnetar/GenAI_Project.git
cd GenAI_Project
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Using venv
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Or using conda
conda create -n neural-grid python=3.12
conda activate neural-grid
```

### Step 3: Install Dependencies

```bash
# Install from src/requirements.txt
pip install -r src/requirements.txt

# For development
pip install -r src/requirements.txt pytest jupyter

# For backend/ML (if using agent planning)
pip install -r End_sem/backend/requirements.txt
```

### Step 4: Verify Installation

```bash
# Test imports
python3 << 'EOF'
import streamlit as st
import joblib
import pandas as pd
import numpy as np
print("✓ All dependencies installed successfully!")
EOF

# Run app
streamlit run src/app.py
```

---

## Usage

### Using Streamlit UI (Recommended)

```bash
cd GenAI_Project
streamlit run src/app.py
```

**Browser Interface** opens at `http://localhost:8501`

#### Tab 1: Manual Prediction
1. Set Hour (0-23) using slider
2. Select Day of Week
3. Enter demand lags (previous hours)
4. Enter optional features (price, grid stability, EV count)
5. Click **RUN INFERENCE**
6. View prediction and 24-hour forecast chart

#### Tab 2: Batch Processing
1. Prepare CSV file with columns:
   - `Datetime` (required)
   - `EV Charging Demand (kW)` (optional)
   - Other features (auto-filled with defaults)
2. Upload CSV via file uploader
3. Preview raw data
4. Click **EXECUTE BATCH INFRASTRUCTURE ANALYSIS**
5. View metrics (R² Score, MAE) and predictions
6. Download results CSV

#### Tab 3: AI Infrastructure Planner
1. Enter Station/Location name
2. Select Planning Horizon (24h, 7d, 30d)
3. Write specific planning query
4. Click **ANALYZE PLANNING** (requires agent module)
5. View AI-generated recommendations

#### Tab 4: Operations Dashboard
1. View real-time metrics (uptime, response time, error rate)
2. Analyze 24-hour demand pattern chart
3. Check weekly analysis bar chart
4. Review active alerts and warnings
5. Monitor system performance

### Using Python API

```python
from pathlib import Path
import pandas as pd
import sys

# Setup paths
PROJECT_ROOT = Path(".").absolute()
BACKEND_PATH = PROJECT_ROOT / "End_sem" / "backend"
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(BACKEND_PATH))

# Import and use model
from src.app import ModelPredictor
import joblib

# Load model
model_bundle = joblib.load("End_sem/backend/models/model_bundle.joblib")
predictor = ModelPredictor(
    model_bundle['estimator'],
    model_bundle['feature_columns'],
    model_bundle['defaults']
)

# Single prediction
result = predictor.predict({
    'Hour': 14,
    'DayOfWeek': 2,
    'Demand_Lag_1': 0.15,
    'Demand_Lag_2': 0.14,
})
print(f"Predicted demand: {result[0]:.4f} kW")

# Batch predictions
df = pd.DataFrame({
    'Hour': [12, 14, 18],
    'DayOfWeek': [0, 2, 4],
})
predictions = predictor.predict(df)
print(f"Batch predictions: {predictions}")
```

---

## Data Formats

### Input CSV Format (for Batch Processing)

Required column:
```csv
Datetime,EV Charging Demand (kW)
2024-01-01 00:00:00,85.5
2024-01-01 01:00:00,72.3
2024-01-01 02:00:00,65.1
```

Optional columns:
```csv
Date,Time,Electricity Price ($/kWh),Grid Stability Index,Number of EVs Charging
2024-01-01,00:00:00,0.12,0.99,5
```

### Output CSV Format (from Batch Processing)

Includes all input features plus predictions:
```csv
Datetime,Hour,DayOfWeek,EV Charging Demand (kW),AI_Predicted_Demand_kW
2024-01-01 00:00:00,0,0,85.5,80.2
2024-01-01 01:00:00,1,0,72.3,75.8
2024-01-01 02:00:00,2,0,65.1,68.4
```

### Sample Datasets

Located in `/data/` directory:
- `Charging station_A_Calif.csv` - Station A historical data
- `Charging station_B_Calif.csv` - Station B historical data
- `Charging station_C_Calif.csv` - Station C historical data

---

## Model Details

### Model Architecture

**WeightedEnsemble** combining:

1. **HistGradientBoostingRegressor**
   - Histogram-based gradient boosting
   - Handles categorical features natively
   - Weight: ~40%

2. **GradientBoostingRegressor**
   - Traditional gradient boosting
   - Sequential tree building
   - Weight: ~60%

### Model Specifications

| Property | Value |
|----------|-------|
| Input Features | 25 |
| Target | EV Charging Demand (kW) |
| Model Type | Ensemble (Weighted) |
| Training Samples | 91,853 |
| Holdout Test Samples | 18,371 |
| R² Score (Full) | 0.5256 |
| MAE (Full) | 0.0706 kW |
| Holdout R² | -0.0687 |
| Holdout MAE | 0.1202 kW |

### Feature Scaling

- **Scaler**: StandardScaler (mean=0, std=1)
- **Fitted on**: Full training dataset
- **Applied to**: All numeric features

### Training Data

- **Date Range**: January - December 2023
- **Frequency**: Hourly measurements
- **Stations**: 3 California EV charging stations
- **Features**: 25-dimensional feature vectors

---

## Troubleshooting

### Issue: "Model Loading Error: Can't get attribute '__pyx_unpickle_CyHalfSquaredError'"

**Cause**: Scikit-learn version mismatch (model was trained with different sklearn version)

**Status**: Fixed - Model has been retrained with current sklearn version

**Solution**: Model has been retrained with current scikit-learn version. The warning should no longer appear. If it does:

1. Clear Streamlit cache:
   ```bash
   rm -rf ~/.streamlit/cache
   ```

2. Restart Streamlit:
   ```bash
   streamlit run src/app.py
   ```

If the issue persists, the fallback statistical model will ensure predictions continue to work.

### Issue: "Model file not found"

**Check**:
```bash
ls -la End_sem/backend/models/model_bundle.joblib
```

**Solution**: Ensure you're running from project root:
```bash
cd GenAI_Project
streamlit run src/app.py
```

### Issue: ImportError for 'agent' module

**Cause**: Optional AI planning module not installed

**Impact**: AI Planning tab shows warning, but other features work normally

**Solution** (optional):
```bash
pip install -r End_sem/backend/requirements.txt
```

### Issue: Port 8501 already in use

**Solution**:
```bash
# Use different port
streamlit run src/app.py --server.port 8502

# Or kill existing Streamlit process
pkill -f streamlit
```

### Issue: Slow batch processing

**Optimization**:
1. Reduce CSV size (process in chunks)
2. Run locally (not cloud) for large files
3. Increase server resources if deployed
4. Use the fallback model for faster inference

### Issue: CSV upload fails

**Check**:
1. Column names match expected format
2. Datetime column is valid and parseable
3. File size < 200MB
4. No special characters in headers

---

## Project Structure

```
GenAI_Project/
│
├── src/                          # Streamlit Application (Primary)
│   ├── app.py                   # Main entry point (8KB)
│   │   ├── ModelPredictor       # Feature auto-fill wrapper
│   │   ├── load_model()         # Load with fallback handling
│   │   ├── preprocess_data()    # Feature engineering
│   │   └── Streamlit Tabs       # UI components
│   │       ├── Tab 1: Manual Prediction
│   │       ├── Tab 2: Batch Processing
│   │       ├── Tab 3: AI Planning
│   │       └── Tab 4: Dashboard
│   ├── utils.py                 # Helper functions
│   ├── requirements.txt          # Dependencies
│   └── .streamlit/              # Streamlit config
│       └── config.toml
│
├── End_sem/backend/             # ML Backend
│   ├── models/                  # Pre-trained models
│   │   ├── model_bundle.joblib  # 10.5 MB ensemble model
│   │   ├── estimator            # WeightedEnsemble
│   │   ├── feature_columns      # 25 feature names
│   │   └── defaults             # Default values per feature
│   │
│   ├── ml/                      # Machine Learning Pipeline
│   │   ├── dataset.py           # Data loader
│   │   ├── preprocessor.py      # Feature engineering
│   │   ├── predictor.py         # Prediction interface
│   │   ├── train.py             # Training script
│   │   └── feature_columns.py   # Feature definitions
│   │
│   ├── agent/                   # Multi-Agent AI System
│   │   ├── run_agent.py         # Agent orchestrator
│   │   ├── graph.py             # Workflow graph
│   │   ├── state.py             # State management
│   │   ├── config.py            # Agent config
│   │   ├── nodes/               # Processing nodes
│   │   │   ├── deep_analysis.py
│   │   │   ├── demand_analyzer.py
│   │   │   ├── evaluator.py
│   │   │   ├── pattern_detector.py
│   │   │   ├── planner.py
│   │   │   ├── rag_retriever.py
│   │   │   ├── reasoning_engine.py
│   │   │   └── simulator.py
│   │   ├── knowledge/           # Knowledge base
│   │   │   ├── ev_planning_rules.txt
│   │   │   └── grid_management_guidelines.txt
│   │   └── utils/               # Agent utilities
│   │       ├── embeddings.py
│   │       ├── llm.py
│   │       └── vector_store.py
│   │
│   ├── data/                    # Training datasets
│   │   ├── Charging station_A_Calif.csv
│   │   ├── Charging station_B_Calif.csv
│   │   └── Charging station_C_Calif.csv
│   │
│   ├── cache/                   # Cached data
│   │   ├── dataset_manifest.json
│   │   ├── engineered_training_df.joblib
│   │   └── uploads/             # User uploaded files
│   │
│   └── main.py                  # Backend API (FastAPI)
│
├── notebooks/                   # Jupyter Notebooks
│   └── milestone_1.ipynb        # Project exploration
│
├── data/                        # Sample Data (Root)
│   ├── Charging station_A_Calif.csv
│   ├── Charging station_B_Calif.csv
│   └── Charging station_C_Calif.csv
│
├── requirements.txt             # Root dependencies
├── README.md                    # Original README
├── README_COMPREHENSIVE.md      # This file
├── ARCHITECTURE_WALKTHROUGH.md  # Architecture details
├── DEPLOYMENT_GUIDE.md          # Deployment instructions
└── .gitignore                   # Git ignore rules
```

---

## Data Flow

### Inference Pipeline

```
User Input (Manual)
├─ Hour: 0-23
├─ DayOfWeek: 0-6
├─ Demand_Lag_1: float
├─ Demand_Lag_2: float
├─ Optional: Price, EV Count, Grid Stability
    ↓
[Calculate Cyclical Features]
├─ hour_sin = sin(2π × hour / 24)
├─ hour_cos = cos(2π × hour / 24)
├─ dow_sin = sin(2π × day / 7)
└─ dow_cos = cos(2π × day / 7)
    ↓
[Build Feature Dictionary]
    ↓
[ModelPredictor Auto-fill Missing]
├─ Apply trained defaults for any missing features
├─ Create 25-feature vector in correct order
    ↓
[Make Prediction]
├─ Input: 25 features
├─ Model: WeightedEnsemble
└─ Output: Demand (kW)
    ↓
[Display Results]
├─ Predicted Demand
├─ Status (Normal/Warning/Alert)
├─ Confidence
└─ 24-Hour Forecast
```

### Batch Pipeline

```
CSV File Upload
    ↓
[Parse & Validate]
├─ Extract Datetime column
├─ Extract/generate Hour, DayOfWeek
├─ Extract EV Charging Demand (target)
    ↓
[Feature Engineering]
├─ Create lags (1, 2, 3 hours)
├─ Calculate rolling statistics
├─ Compute cyclical features
├─ Add interaction terms
├─ Impute defaults for missing features
    ↓
[Build 25-Feature Matrix]
    ↓
[Batch Predictions]
├─ Predict for all rows
├─ Add predictions to DataFrame
    ↓
[Quality Metrics]
├─ R² Score
├─ Mean Absolute Error
├─ Residuals
    ↓
[Output]
└─ CSV with predictions + metrics
```

---

## Contributing

### Bug Reports

Please report bugs with:
1. Reproduction steps
2. Expected vs actual behavior
3. System info (OS, Python version, sklearn version)
4. Error traceback

### Feature Requests

Suggestions welcome for:
- Additional prediction features
- New visualization types
- Performance optimizations
- UI/UX improvements

### Code Contributions

1. Fork the repository
2. Create feature branch: `git checkout -b feature/YourFeature`
3. Make changes with tests
4. Submit pull request with description

---

## License

[Your License Here - e.g., MIT, Apache 2.0, etc.]

---

## Team & Credits

**Project**: NEURAL GRID - EV Demand Forecasting System
**Institution**: Rishihood University
**Last Updated**: April 2026

### Technologies Used

- **ML Framework**: Scikit-Learn
- **Frontend**: Streamlit, React (Vite)
- **Backend**: Python, FastAPI
- **AI Agents**: LangChain, OpenAI/Mistral
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly, Matplotlib
- **Deployment**: Render, Docker
- **Version Control**: Git/GitHub

---

## Support

For issues or questions:
1. Check [Troubleshooting](#troubleshooting) section
2. Review error logs: `streamlit run src/app.py --logger.level=debug`
3. Open GitHub issue with details
4. Contact project team

---

## Future Roadmap

- [ ] Real-time API endpoint
- [ ] Mobile app integration
- [ ] Advanced weather integration
- [ ] Grid pricing optimization
- [ ] Predictive maintenance alerts
- [ ] Multi-site coordination
- [ ] Advanced time-series forecasting (LSTM)
- [ ] Model retraining pipeline automation

---

**Made with care for EV Infrastructure Optimization**
