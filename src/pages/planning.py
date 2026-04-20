"""Tab 3: Agent Planning"""

import streamlit as st
import pandas as pd
from models import agent_runner
from components import section_header, alert_box

def show():
    """Display agent planning tab."""
    st.header("🤖 Agent Planning")
    
    if agent_runner is None:
        alert_box("Agent system not available", "warning")
        return
    
    section_header("Planning Query")
    
    col1, col2 = st.columns(2)
    
    with col1:
        location = st.text_input(
            "Location/Station",
            value="Charging Station A, California"
        )
    
    with col2:
        time_horizon = st.selectbox(
            "Planning Horizon",
            ["Next 24 hours", "Next 7 days", "Next 30 days"]
        )
    
    query = st.text_area(
        "Planning Query",
        value="What are the optimal charging patterns for tomorrow?",
        height=100
    )
    
    if st.button("🔄 Generate Plan", key="planning_btn"):
        with st.spinner("Agent analyzing..."):
            try:
                # Prepare context
                context = {
                    'location': location,
                    'horizon': time_horizon,
                    'query': query
                }
                
                # Run agent workflow
                result = agent_runner(context)
                
                if result:
                    st.success("✅ Planning complete")
                    
                    # Display results
                    section_header("Generated Plan")
                    
                    if isinstance(result, dict):
                        st.json(result)
                    else:
                        st.write(result)
                    
                    # Recommendations
                    section_header("Key Recommendations")
                    
                    recommendations = [
                        "✓ Increase capacity during peak hours (3-6 PM)",
                        "✓ Schedule maintenance during low demand (11 PM - 6 AM)",
                        "✓ Monitor Grid load for potential bottlenecks"
                    ]
                    
                    for rec in recommendations:
                        st.write(rec)
                
                else:
                    alert_box("No plan generated", "warning")
                
            except Exception as e:
                alert_box(f"Agent error: {str(e)}", "error")
    
    # History
    if 'planning_history' not in st.session_state:
        st.session_state.planning_history = []
    
    section_header("Recent Plans")
    
    if st.session_state.planning_history:
        history_df = pd.DataFrame(st.session_state.planning_history)
        st.dataframe(history_df, use_container_width=True, hide_index=True)
    else:
        st.info("No plans generated yet")
