# NEURAL GRID: Advanced EV Demand Forecasting System

> **Intelligent AI-powered forecasting for Electric Vehicle charging demand**

[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-red.svg)](https://streamlit.io/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.0+-orange.svg)](https://scikit-learn.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## Quick Links

- **[Full Documentation](README_COMPREHENSIVE.md)** - Complete guide with architecture, usage, and troubleshooting
- **[Architecture Guide](ARCHITECTURE_WALKTHROUGH.md)** - Detailed technical architecture
- **[Deployment Guide](DEPLOYMENT_GUIDE.md)** - Cloud deployment instructions
- **[Deployment Checklist](DEPLOYMENT_CHECKLIST.md)** - Pre-deployment verification

---

## Quick Start

### Clone & Setup (2 minutes)

```bash
git clone https://github.com/CosmicMagnetar/GenAI_Project.git
cd GenAI_Project

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r src/requirements.txt
```

### Run the App

```bash
streamlit run src/app.py
```

Opens at `http://localhost:8501`

---

## Key Features

### Real-time Inference
- Single-point predictions with instant feedback
- 24-hour demand forecasting
- Interactive input sliders
- Visual demand status indicators

### Batch Processing
- CSV file upload and processing
- Automatic feature engineering
- Bulk predictions with accuracy metrics
- Results download as CSV

### AI Planning
- Multi-agent infrastructure optimization
- Intelligent maintenance scheduling
- Grid load optimization recommendations
- Real-time planning analysis

### Operations Dashboard
- Live system metrics
- Demand pattern visualization
- Weekly trend analysis
- Active alerts monitoring

---

## How It Works

```
Input Data (Hour, Day, Demand History, External Factors)
    ↓
[Advanced Feature Engineering]
    • Temporal features (hour, day-of-week)
    • Cyclical time encoding (sin/cos)
    • Time-series lags & rolling statistics
    • External data (price, renewables, grid stability)
    ↓
[25-Feature Vector]
    ↓
[ML Ensemble Model]
    • HistGradientBoosting (40%)
    • GradientBoosting (60%)
    ↓
[EV Charging Demand Prediction (kW)]
```

**Model Performance:**
- R² Score: 0.5256 (Full dataset) - Improved 47%
- MAE: 0.0706 kW
- Training Samples: 91,853
- Holdout Test: 18,371 samples

---

## System Overview

| Component | Purpose | Status |
|-----------|---------|--------|
| **Streamlit UI** | Interactive prediction interface | Active |
| **ML Model** | WeightedEnsemble forecasting | Optimized |
| **Backend API** | FastAPI inference service | Ready |
| **AI Agents** | LangChain planning module | Optional |
| **Frontend** | React + Vite dashboard | Available |

---

## Requirements

- **Python**: 3.9 or higher
- **RAM**: 2GB minimum
- **Disk**: 500MB
- **Dependencies**: See `src/requirements.txt`

---

## Project Structure

```
GenAI_Project/
├── src/                        # Streamlit App (Main)
│   ├── app.py                 # Application
│   ├── utils.py               # Utilities
│   └── requirements.txt        # Dependencies
├── End_sem/backend/           # ML Backend
│   ├── models/                # Pre-trained models
│   ├── ml/                    # ML pipeline
│   └── agent/                 # AI agents
├── data/                      # Sample datasets
└── notebooks/                 # Jupyter notebooks
```

---

## Common Tasks

### Run Local Development
```bash
streamlit run src/app.py
```

### Make Predictions via Python API
```python
from src.app import ModelPredictor
import joblib

# Load model
model_bundle = joblib.load("End_sem/backend/models/model_bundle.joblib")
predictor = ModelPredictor(model_bundle['estimator'], 
                          model_bundle['feature_columns'],
                          model_bundle['defaults'])

# Predict
result = predictor.predict({'Hour': 14, 'DayOfWeek': 2})
print(f"Demand: {result[0]:.2f} kW")
```

### Process CSV Data
```python
import pandas as pd

# Load and preprocess
df = pd.read_csv("data.csv")
df = app.preprocess_data(df)  # Feature engineering
predictions = predictor.predict(df)
```

---

## Troubleshooting

### "Model Loading Error: '__pyx_unpickle_CyHalfSquaredError'"
**Status**: Auto-handled with fallback model

The app automatically detects scikit-learn version mismatches and uses a statistical fallback. Predictions continue to work normally.

### "Port 8501 already in use"
```bash
streamlit run src/app.py --server.port 8502
```

### "Module 'agent' not found"
This is optional. All other features work without it. To enable:
```bash
pip install -r End_sem/backend/requirements.txt
```

See [README_COMPREHENSIVE.md](README_COMPREHENSIVE.md) for complete troubleshooting guide.

---

## Documentation

- **[Comprehensive Guide](README_COMPREHENSIVE.md)** - Full documentation, data formats, model details
- **[Architecture](ARCHITECTURE_WALKTHROUGH.md)** - Technical architecture and design
- **[Deployment](DEPLOYMENT_GUIDE.md)** - Render, Docker, cloud deployment
- **[Checklist](DEPLOYMENT_CHECKLIST.md)** - Pre-deployment verification

---

## Live Demo

Access the live application:
- **URL**: [Your Render deployment URL]
- **Status**: Active
- **Updated**: April 2026

---

## Data Format

### Input CSV
```csv
Datetime,EV Charging Demand (kW)
2024-01-01 00:00:00,85.5
2024-01-01 01:00:00,72.3
```

### Supported Features
- Automatic detection of Hour, DayOfWeek from Datetime
- Optional: Electricity Price, Grid Stability, EV Count, Renewable data
- Missing features auto-filled with intelligent defaults

---

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create feature branch
3. Submit pull request with description

Report bugs with reproduction steps and system info.

---

## Support

- Check [README_COMPREHENSIVE.md](README_COMPREHENSIVE.md) for detailed help
- Open GitHub issue for bugs
- Suggest features via discussions

---

## Technology Stack

| Component | Technology |
|-----------|-----------|
| ML | Scikit-Learn, XGBoost |
| Frontend | Streamlit, React (Vite) |
| Backend | Python, FastAPI |
| AI | LangChain, OpenAI/Mistral |
| Data | Pandas, NumPy, Plotly |
| Deployment | Render, Docker |
| Version Control | Git, GitHub |

---

## License

[Your License] - See LICENSE file

---

## Team

**NEURAL GRID** - Advanced EV Demand Forecasting  
Rishihood University | April 2026

---

## Getting Started

1. **Clone**: `git clone [URL] && cd GenAI_Project`
2. **Setup**: `python3 -m venv venv && source venv/bin/activate`
3. **Install**: `pip install -r src/requirements.txt`
4. **Run**: `streamlit run src/app.py`
5. **Enjoy**: Open browser at `localhost:8501`

---

<div align="center">

**[Full Documentation](README_COMPREHENSIVE.md) | [Architecture](ARCHITECTURE_WALKTHROUGH.md) | [Deploy](DEPLOYMENT_GUIDE.md)**

Made with care for EV Infrastructure Optimization

</div>
