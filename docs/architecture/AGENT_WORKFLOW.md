# Agent Workflow Diagrams

This document contains visual representations of the agent workflow and system architecture.

## Agent Workflows

### 1. Inference Pipeline
Shows how user input flows through the ML prediction system:
```
User Input (Manual/Batch/API)
    ↓
Input Processor
    ↓
Feature Engineering (Temporal, Cyclical, Lags, Rolling Stats, Interactions)
    ↓
Data Validation & Auto-filling
    ↓
StandardScaler Normalization
    ↓
Ensemble Model
    ├─ HistGradientBoosting (60%)
    └─ GradientBoosting (40%)
    ↓
Weighted Average (0.6 × pred1 + 0.4 × pred2)
    ↓
Output: EV Charging Demand Prediction
    ↓
Streamlit UI Display Results
```

### 2. Agent Node Workflow (LangGraph)
Shows the multi-step agent reasoning process:
```
Start Agent Flow
    ↓
RAG Retriever Node (Load Knowledge Base)
    ↓
Demand Analyzer (Analyze Historical Data, Identify Patterns)
    ↓
Pattern Detector (Find Trends, Seasonal Patterns)
    ↓
Reasoning Engine (Process Logic, Generate Insights)
    ↓
Simulator Node (Forecast Scenarios, Model Outcomes)
    ↓
Planner Node (Create Action Plan, Optimize Resources)
    ↓
Evaluator Node (Assess Results, Quality Metrics)
    ↓
Deep Analysis (Detailed Insights, Risk Assessment)
    ↓
Final Report (Recommendations, Action Items)
```

### 3. System Architecture Overview
Shows the complete system layers:
```
USER INTERFACE LAYER:
├─ Streamlit Dashboard
├─ React Frontend
└─ Operations Panel

    ↓

FEATURE ENGINEERING LAYER:
├─ Temporal Processing
├─ Cyclical Encoding
├─ Lag Features
├─ Rolling Statistics
└─ Interaction Terms

    ↓

DATA PROCESSING (25-Dimensional Feature Vector)

    ↓

PREPROCESSING (StandardScaler Normalization)

    ↓

ML MODEL LAYER:
├─ HistGradientBoosting (60%)
├─ GradientBoosting (40%)
└─ Weighted Ensemble

    ↓

OUTPUT (EV Charging Demand Prediction)
```

### 4. Data Pipeline & Feature Engineering
Shows the data flow from raw inputs to predictions:
```
Raw Data Sources:
├─ Charging Station A (CSV)
├─ Charging Station B (CSV)
├─ Charging Station C (CSV)
└─ External Data (Weather, Prices, Grid)

    ↓

Data Loading & Merging

    ↓

Feature Engineering Pipeline:
├─ Temporal Features (hour, day_of_week, sin/cos)
├─ Time-Series Features (lag_1, lag_2, lag_3)
├─ Rolling Statistics (avg_3h, avg_6h, std_3h)
├─ External Features (price, grid_stability, ev_count, solar, wind)
└─ Infrastructure Features (capacity, peak_demand, renewable%, battery)

    ↓

25-Dimensional Feature Vector

    ↓

StandardScaler Normalization

    ↓

ML Ensemble Model (HistGB + GBR)

    ↓

EV Charging Demand Prediction Output
```

## AI Image Generation Instructions

### Image 1: Agent Inference Pipeline
**File**: `agent_inference_pipeline.png`
**Prompt**:
```
Create a professional technical flowchart showing EV charging demand prediction pipeline.
Top: Three input types (manual controls, CSV file upload, API request).
Flow: Input Processor → Feature Engineering box with sub-components 
(temporal, cyclical, lags, rolling stats, interactions) → Data Validation 
→ StandardScaler → Ensemble Model splitting to HistGradientBoosting (60%) 
and GradientBoosting (40%) → Weighted averaging → Output prediction.
Bottom: Streamlit UI display.
Dark professional background, bright cyan/magenta/orange accents, clean vector style.
Resolution: 1200x800px minimum. Format: PNG.
```

### Image 2: LangGraph Agent Nodes
**File**: `langgraph_agent_workflow.png`
**Prompt**:
```
Create a technical diagram showing agent reasoning workflow with 9 connected nodes.
Sequential flow: RAG Retriever → Demand Analyzer → Pattern Detector → Reasoning Engine 
→ Simulator → Planner → Evaluator → Deep Analysis → Final Report Output.
Each node should show its function clearly. Dark theme with cyan connecting lines and 
color-coded node boxes (different colors for each stage). Professional style.
Resolution: 1200x800px minimum. Format: PNG.
```

### Image 3: System Architecture Layers
**File**: `system_architecture_layers.png`
**Prompt**:
```
Create a layered system architecture diagram with 6 horizontal layers.
Layer 1 (Top): User Interface (Streamlit, React, Operations Dashboard)
Layer 2: Feature Engineering (Temporal, Cyclical, Lags, Rolling, Interactions)
Layer 3: Feature Vector (25 dimensions)
Layer 4: Preprocessing (StandardScaler)
Layer 5: ML Models (HistGB 60%, GBR 40%, Weighted Ensemble)
Layer 6: Output (Prediction)
Show data flow arrows between layers. Dark background, bright accents, professional.
Resolution: 1200x800px minimum. Format: PNG.
```

### Image 4: Data Pipeline & Features
**File**: `data_pipeline_features.png`
**Prompt**:
```
Create a data pipeline flowchart starting with 4 data sources (3 charging stations + external data).
Show merging into Data Loading stage, then branching into Feature Engineering 
with 5 sub-processes (Temporal, Time-Series, Rolling Stats, External, Infrastructure).
Converge to 25-feature vector → StandardScaler → Ensemble Model → Prediction output.
Dark theme, cyan data flow arrows, color-coded feature groups, professional style.
Resolution: 1200x800px minimum. Format: PNG.
```

## How to Generate Images

### Option 1: DALL-E (OpenAI)
1. Go to https://openai.com/dall-e-3/
2. Copy the prompt above for the image you want
3. Paste into DALL-E prompt box
4. Generate image
5. Download as PNG

### Option 2: Midjourney
1. Go to https://www.midjourney.com/
2. Use command: `/imagine [prompt text]`
3. Adjust as needed
4. Download final result as PNG

### Option 3: Stable Diffusion
1. Visit https://stablediffusionweb.com/ or use local installation
2. Paste prompt
3. Generate image
4. Download as PNG

## How to Add Images to Repository

1. Generate 4 PNG images using the prompts above
2. Save them to `docs/architecture/` folder with exact filenames:
   - `agent_inference_pipeline.png`
   - `langgraph_agent_workflow.png`
   - `system_architecture_layers.png`
   - `data_pipeline_features.png`

3. Run these commands:
```bash
cd /Users/krishna./Downloads/GenAI_Project-main\ 3
git add docs/architecture/*.png
git commit -m "ADD: AI-generated agent workflow and architecture diagram images"
git push origin main
```

4. Images will automatically display in README.md via markdown links

## Agent Components Reference

### Nodes (agent/nodes/)
- **rag_retriever.py**: Retrieves knowledge from vector store
- **demand_analyzer.py**: Analyzes historical charging demand patterns
- **pattern_detector.py**: Detects seasonal and trend patterns
- **reasoning_engine.py**: Processes logic and generates insights
- **simulator.py**: Forecasts scenarios and models outcomes
- **planner.py**: Creates optimization plans and resource allocation
- **evaluator.py**: Assesses results and calculates quality metrics
- **deep_analysis.py**: Detailed analysis with risk assessment

### Graph Flow (agent/graph.py)
- Orchestrates node execution in LangGraph
- Manages state transitions between nodes
- Combines outputs for final recommendations

### State Management (agent/state.py)
- Maintains agent execution state
- Tracks input/output at each node
- Stores intermediate results

## Technologies Used

- **LangGraph**: Multi-agent orchestration
- **LangChain**: LLM integration
- **Vector Store**: Knowledge base retrieval
- **Feature Engineering**: 25-dimensional input vectors
- **ML Ensemble**: Weighted HistGradientBoosting + GradientBoosting
- **Streamlit**: Web UI for predictions
- **React**: Frontend dashboard
