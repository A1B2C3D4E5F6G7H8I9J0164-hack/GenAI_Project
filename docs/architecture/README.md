# Architecture Diagrams

This folder contains AI-generated architecture diagrams for the NEURAL GRID project documentation.

## Images to Add

### 1. system_architecture.png
**Description**: Multi-layered system architecture diagram
**Should show**:
- User Interface Layer (Streamlit, React, Operations Dashboard)
- Feature Engineering Layer with data transformations
- 25-Dimensional Feature Vector
- ML Model Layer (HistGradientBoosting + GradientBoosting)
- Prediction Output (EV Charging Demand)
- Data flowing downward through each layer

**Style**: Professional flowchart with color-coded layers

### 2. data_pipeline.png
**Description**: Data processing pipeline from raw to prediction
**Should show**:
- Raw CSV Data inputs (Charging stations A, B, C + External data)
- Data Loading & Merging step
- Feature Engineering processes:
  - Temporal features
  - Cyclical encoding (sin/cos)
  - Time-series lags
  - Rolling statistics
  - Interaction terms
- Feature Vector generation (25 dimensions)
- StandardScaler normalization
- Ensemble Model processing
- Final EV Demand Prediction output

**Style**: Step-by-step pipeline with clear progression

### 3. model_architecture.png
**Description**: ML model structure and components
**Should show**:
- Input: 25 Features categorized by type
  - Temporal (4): Hour, DayOfWeek, hour_sin, hour_cos, dow_sin, dow_cos
  - Time-Series (3): Demand_Lag_1, Demand_Lag_2, Demand_Lag_3
  - Rolling Stats (3): Rolling_Avg_3h, Rolling_Avg_6h, Rolling_Std_3h
  - External (9): Price, Grid_Stability, EV_Count, Solar, Wind, etc.
  - Infrastructure (4): Capacity, Peak_Demand, Renewable%, Battery_Storage
- StandardScaler Normalization layer
- Weighted Ensemble section showing:
  - HistGradientBoostingRegressor (60% weight)
  - GradientBoostingRegressor (40% weight)
  - Weighted averaging (0.6 × pred1 + 0.4 × pred2)
- Output: EV Charging Demand (kW)
- Performance metrics box

**Style**: Detailed technical architecture diagram

### 4. inference_flow.png
**Description**: Prediction inference process
**Should show**:
- Three input paths:
  - Manual: Interactive sliders (Hour, DayOfWeek, demand history)
  - Batch: CSV file upload
  - API: JSON payload
- Feature Validation & Auto-filling step
- StandardScaler Transform
- Ensemble Prediction split:
  - 60% HistGradientBoosting path
  - 40% GradientBoosting path
  - Weighted Average combination
- Output: EV Charging Demand (kW)

**Style**: Process flow diagram with decision points and merging paths

## How to Generate Images

### Using DALL-E (OpenAI)
```
Prompt for each diagram:
"Create a professional [diagram type] for an EV charging demand forecasting system. 
Show [specific components]. Use a dark theme with bright accent colors (cyan, magenta, orange). 
Style: clean, technical, modern."
```

### Using Midjourney
```
/imagine "Technical architecture diagram of an EV demand forecasting system. 
[Specific details]. Professional dark theme. Clean layout. Vector style."
```

### Using Stable Diffusion
```
"Technical system architecture diagram, AI machine learning model, 
dark theme professional visualization, [specific components]"
```

## File Format Requirements

- **Format**: PNG (transparency preferred)
- **Resolution**: Minimum 1200x800px (preferably 1920x1080px)
- **Size**: Keep under 5MB per image
- **Colors**: Dark theme with bright accents (cyan #00f2ff, magenta #ff00ff, orange #ff9900)

## Example Prompts for Image Generation

### System Architecture
"Create a technical diagram showing a multi-layer machine learning system. 
Top layer: User Interface with Streamlit dashboard, React frontend, Operations dashboard. 
Middle layers: Feature engineering, 25-dimensional feature vector, ML model layer. 
Bottom: Prediction output. Dark theme with cyan borders. Professional style."

### Data Pipeline
"Technical data pipeline diagram for EV charging data processing. 
Show: Raw CSV data from 3 charging stations and external data feeds → Data merging → 
Feature engineering (temporal, cyclical, lags, rolling stats, interactions) → 
25-feature vector → StandardScaler → Ensemble model → EV demand prediction. 
Dark background, bright accent colors, arrows showing data flow."

### Model Architecture
"Machine learning model architecture diagram. Show input layer with 25 features 
(categorized), preprocessing layer with StandardScaler, model layer with 
HistGradientBoosting (60%) and GradientBoosting (40%) with weighted average, 
output layer showing EV demand prediction. Include performance metrics box. 
Dark theme, professional, technical style."

### Inference Flow
"Flowchart showing three input types (manual controls, CSV batch, API request) 
flowing through feature validation, StandardScaler normalization, ensemble prediction 
(splitting to HistGB and GB paths, then weighted averaging), producing EV demand 
output. Dark theme, color-coded paths, professional style."

## Adding Images to README

Once generated, place PNG files in this directory. The README_COMPREHENSIVE.md 
will automatically reference them with:

```markdown
![System Architecture](docs/architecture/system_architecture.png)
```

Images will display when the README is viewed on GitHub.
