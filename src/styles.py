"""Global styling for NEURAL GRID application."""

MAIN_STYLES = """
<style>
:root {
  --primary: #0ea5e9;
  --secondary: #a855f7;
  --accent: #34d399;
  --danger: #f43f5e;
  --dark-bg: #0f0f19;
  --light-text: #f1f5f9;
}

body {
  background: linear-gradient(135deg, #0f0f19 0%, #1a1a2e 100%);
}

.glass-card {
  background: rgba(15, 15, 25, 0.7) !important;
  backdrop-filter: blur(10px) !important;
  border: 1px solid rgba(14, 165, 233, 0.15) !important;
  border-radius: 12px !important;
  padding: 1.5rem !important;
  margin: 0.5rem 0 !important;
  transition: all 0.3s ease !important;
}

.glass-card:hover {
  background: rgba(15, 15, 25, 0.85) !important;
  border-color: rgba(14, 165, 233, 0.3) !important;
  box-shadow: 0 8px 32px rgba(14, 165, 233, 0.1) !important;
}

.gradient-title {
  background: linear-gradient(120deg, #0ea5e9, #a855f7);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-weight: 800;
  font-size: 3.5rem;
  margin-bottom: 0.5rem;
}

.gradient-subtitle {
  background: linear-gradient(120deg, #34d399, #0ea5e9);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-size: 1.25rem;
  font-weight: 600;
}

.metric-card {
  background: linear-gradient(135deg, rgba(14, 165, 233, 0.1), rgba(168, 85, 247, 0.1));
  border-left: 4px solid #0ea5e9;
  padding: 1.25rem;
  border-radius: 10px;
  margin: 0.5rem 0;
}

.stButton button {
  background: linear-gradient(135deg, #0ea5e9, #06b6d4);
  border: none;
  border-radius: 8px;
  font-weight: 600;
  transition: all 0.3s ease;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  padding: 0.75rem 1.5rem !important;
}

.stButton button:hover {
  background: linear-gradient(135deg, #06b6d4, #0ea5e9);
  box-shadow: 0 8px 24px rgba(14, 165, 233, 0.3);
  transform: translateY(-2px);
}

.section-title {
  color: #0ea5e9;
  font-size: 1.5rem;
  font-weight: 700;
  margin: 1.5rem 0 1rem 0;
  padding-bottom: 0.75rem;
  border-bottom: 2px solid rgba(14, 165, 233, 0.3);
}

.stTabs {
  margin-top: 1.5rem;
}

[data-baseweb="tab"] {
  border-radius: 8px 8px 0 0;
  font-weight: 600;
  padding: 0.75rem 1.5rem !important;
}

[data-baseweb="tab"][aria-selected="true"] {
  background: linear-gradient(135deg, #0ea5e9, #a855f7);
}

.stNumberInput input, .stSlider input {
  border-radius: 8px;
  border: 1px solid rgba(14, 165, 233, 0.3);
}

.stFileUploader {
  border-radius: 12px;
  border: 2px dashed rgba(14, 165, 233, 0.3);
}

.stFileUploader:hover {
  border-color: rgba(14, 165, 233, 0.6);
  background: rgba(14, 165, 233, 0.05);
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
  background: rgba(244, 63, 94, 0.2);
  color: #f43f5e;
  border: 1px solid #f43f5e;
}

.streamlit-expanderHeader {
  border-radius: 8px;
  background: rgba(14, 165, 233, 0.1);
  border: 1px solid rgba(14, 165, 233, 0.2);
}

.stSuccess {
  background: rgba(16, 185, 129, 0.1);
  border-left: 4px solid #10b981;
}

.stError {
  background: rgba(244, 63, 94, 0.1);
  border-left: 4px solid #f43f5e;
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
}
</style>
"""
