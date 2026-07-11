import streamlit as st
import pandas as pd
import json
from pathlib import Path
import altair as alt

st.set_page_config(page_title="EduScore MLOps Dashboard", layout="wide")

# Paths relative to the project root (where Streamlit will be run)
PREDICTION_LOG_PATH = Path("monitoring/predictions.jsonl")
REFERENCE_PATH = Path("models/training_reference.json")

def load_data():
    if not PREDICTION_LOG_PATH.exists():
        return pd.DataFrame()
    
    with open(PREDICTION_LOG_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    events = [json.loads(line) for line in lines if line.strip()]
    if not events:
        return pd.DataFrame()
        
    df = pd.DataFrame(events)
    # Extract nested features
    features_df = pd.json_normalize(df['features'])
    df = pd.concat([df.drop(columns=['features']), features_df], axis=1)
    
    # Convert timestamp to datetime
    df['datetime'] = pd.to_datetime(df['timestamp'], unit='s')
    return df

def load_reference():
    if not REFERENCE_PATH.exists():
        return {}
    with open(REFERENCE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

# Use Streamlit 1.37+ fragment auto-refresh for a live feed
@st.fragment(run_every="5s")
def render_dashboard():
    df = load_data()
    reference = load_reference()
    
    st.title("EduScore MLOps Dashboard 🎓")
    
    if df.empty:
        st.warning("No predictions found yet. Make some requests to the API!")
        return
        
    st.markdown(f"*Last updated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')} (Auto-refreshing every 5s)*")
    
    # Top-Level Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Predictions", len(df))
    with col2:
        st.metric("Avg Predicted Score", f"{df['predicted_score'].mean():.2f}")
    with col3:
        st.metric("Avg Latency (ms)", f"{df['latency_ms'].mean():.2f}")
        
    st.divider()
    
    # Time-Series Analysis
    st.subheader("Prediction Trends Over Time")
    
    # Line chart for predicted scores
    chart = alt.Chart(df).mark_line(point=True).encode(
        x=alt.X('datetime:T', title='Time'),
        y=alt.Y('predicted_score:Q', title='Predicted Score', scale=alt.Scale(domain=[0, 100])),
        tooltip=['datetime', 'predicted_score', 'predicted_grade']
    ).properties(height=300)
    
    st.altair_chart(chart, use_container_width=True)
    
    st.divider()
    
    # Drift Detection Visualization
    st.subheader("Feature Drift Detection")
    
    if "feature_means" in reference:
        ref_means = reference["feature_means"]
        
        # Make sure we only calculate means for features that actually exist in the dataframe
        available_features = [f for f in ['study_hours', 'attendance_percentage', 'class_participation'] if f in df.columns]
        current_means = df[available_features].mean().to_dict()
        
        # Prepare data for plotting
        drift_data = []
        for feature in ref_means.keys():
            if feature in current_means:
                drift_data.append({"Feature": feature, "Source": "Training Reference", "Mean Value": ref_means[feature]})
                drift_data.append({"Feature": feature, "Source": "Production (Current)", "Mean Value": current_means[feature]})
                
        if drift_data:
            drift_df = pd.DataFrame(drift_data)
            
            # Grouped bar chart
            bar_chart = alt.Chart(drift_df).mark_bar().encode(
                x=alt.X('Source:N', title=None, axis=alt.Axis(labels=False)),
                y=alt.Y('Mean Value:Q'),
                color='Source:N',
                column=alt.Column('Feature:N', header=alt.Header(title=None, labelOrient='bottom'))
            ).properties(width=200, height=300)
            
            st.altair_chart(bar_chart)
        else:
            st.info("Waiting for data matching the training features...")
    else:
        st.info("No training reference found. Train the model to enable drift detection.")
        
    st.divider()
    st.subheader("Recent Predictions Log")
    # Display the most recent 10 predictions
    st.dataframe(
        df.sort_values(by='datetime', ascending=False)
        .drop(columns=['timestamp'])
        .head(10), 
        use_container_width=True
    )

# Main app execution
render_dashboard()
