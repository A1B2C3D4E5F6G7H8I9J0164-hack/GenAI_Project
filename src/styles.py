"""Global styling for NEURAL GRID application."""

MAIN_STYLES = """
<style>
:root {
  --primary: #ff003c;
  --secondary: #b3002a;
  --accent: #00f2ff;
  --danger: #ff003c;
  --dark-bg: #000000;
  --light-text: #e0e0e0;
}

body {
  background: #000000;
  font-family: 'Inter', sans-serif;
}

/* Base header and text styling */
h1, h2, h3, h4 {
    font-weight: 700 !important;
    text-transform: uppercase;
    letter-spacing: -0.5px;
}

.glass-card {
  background: rgba(15, 15, 15, 0.7) !important;
  border: 1px solid rgba(255, 0, 60, 0.15) !important;
  border-radius: 8px !important;
  padding: 1.5rem !important;
  margin: 0.5rem 0 !important;
  transition: all 0.3s ease !important;
}

.glass-card:hover {
  background: rgba(20, 20, 20, 0.85) !important;
  border-color: rgba(255, 0, 60, 0.4) !important;
}

.gradient-title {
  color: #ffffff;
  font-weight: 800;
  font-size: 3.5rem;
  margin-bottom: 0.5rem;
}

.gradient-subtitle {
  color: #888888;
  font-size: 1.25rem;
  font-weight: 600;
  text-transform: uppercase;
}

.metric-card {
  background: transparent;
  border-left: 4px solid #ff003c;
  padding: 1.25rem;
  border-radius: 4px;
  margin: 0.5rem 0;
}

/* Slider customized to match the red theme in the reference */
.stSlider div[data-testid="stThumbValue"] {
    color: #ffffff;
}
.stSlider div[data-baseweb="slider"] {
    padding-top: 10px;
}
.stSlider div[data-baseweb="slider"] > div:nth-child(1) {
    background-color: rgba(255, 51, 102, 0.2) !important;
}
.stSlider div[data-baseweb="slider"] > div:nth-child(2) > div {
    background-color: #ff003c !important;
}

/* Input boxes with dark grey backgrounds */
div[data-baseweb="input"] {
    background-color: #2b2b36 !important;
    border: none;
    border-radius: 6px;
    color: white;
}

.stButton button {
    background: transparent !important;
    color: #ff003c !important;
    border: 1px solid #ff003c !important;
    border-radius: 4px !important;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    transition: all 0.3s ease;
}

.stButton button:hover {
    background: rgba(255, 0, 60, 0.1) !important;
    box-shadow: 0 0 15px rgba(255, 0, 60, 0.4) !important;
}

.section-title {
  color: #ff003c;
  font-size: 1.5rem;
  font-weight: 700;
  margin: 1.5rem 0 1rem 0;
  padding-bottom: 0.75rem;
}

.stTabs {
  margin-top: 1.5rem;
}

[data-baseweb="tab"] {
    color: #888888 !important;
    font-weight: 600;
    background: transparent;
    padding-top: 15px;
    padding-bottom: 15px;
}

[data-baseweb="tab"][aria-selected="true"] {
    color: #ff003c !important;
    border-bottom: 2px solid #ff003c !important;
    background: transparent !important;
}

.stNumberInput input, .stSlider input {
  border-radius: 6px;
  border: 1px solid rgba(255, 0, 60, 0.3);
}

.stFileUploader {
  border-radius: 8px;
  border: 2px dashed rgba(255, 0, 60, 0.4);
}

.stFileUploader:hover {
  border-color: rgba(255, 0, 60, 0.6);
  background: rgba(255, 0, 60, 0.05);
}

.status-badge {
  display: inline-block;
  padding: 0.35rem 0.85rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
  margin-right: 0.5rem;
}

.status-online {
  background: rgba(16, 185, 129, 0.2);
  color: #10b981;
  border: 1px solid #10b981;
}

.status-alert {
  background: rgba(255, 0, 60, 0.2);
  color: #ff003c;
  border: 1px solid #ff003c;
}

.streamlit-expanderHeader {
  border-radius: 4px;
  background: rgba(255, 0, 60, 0.1);
  border: 1px solid rgba(255, 0, 60, 0.2);
}

.stSuccess {
  background: rgba(16, 185, 129, 0.1);
  border-left: 4px solid #10b981;
}

.stError {
  background: rgba(255, 0, 60, 0.1);
  border-left: 4px solid #ff003c;
}

.stWarning {
  background: rgba(250, 204, 21, 0.1);
  border-left: 4px solid #facc15;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.stMetricValue {
  animation: fadeIn 0.5s ease-out;
  color: #ff003c !important;
}
.stMetricLabel {
    color: #888888 !important;
    text-transform: uppercase;
}
</style>
"""
