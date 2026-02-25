# ============================
# AI Project Failure Predictor - Streamlit Dashboard
# UI: Upload-First, Description, Dynamic Results
# ============================

import streamlit as st
import pandas as pd

# Import placeholder modules
import ml_model
import visuals
import utils

# ---------------------------
# Streamlit Page Setup
# ---------------------------
st.set_page_config(page_title="AI Project Failure Predictor", layout="wide")

# ---------------------------
# Sidebar - CSV Upload
# ---------------------------
st.sidebar.title("Project Input")
uploaded_file = st.sidebar.file_uploader("Upload CSV file", type="csv")

# ---------------------------
# Main Page Header
# ---------------------------
st.title("AI Project Failure Predictor")
st.markdown("""
This dashboard predicts task-level and project-level risks, 
highlights critical tasks, and provides actionable suggestions 
to help you manage your project efficiently.
""")

# ---------------------------
# Upload-First Behavior
# ---------------------------
if uploaded_file is None:
    st.info("Please upload your project CSV to see the results.")
    st.stop()  # Wait until user uploads a file
else:
    df = pd.read_csv(uploaded_file)

# ---------------------------
# Generate Placeholder Risk Scores
# ---------------------------
df = ml_model.generate_risk_scores(df)

# ---------------------------
# Categorize Risk Using Utils Module
# ---------------------------
df['RiskCategory'] = df['RiskScore'].apply(utils.categorize_risk)

# ---------------------------
# Add Emoji-Based Risk Indicator
# ---------------------------
color_map = {
    "Low": "🟩 Low",
    "Medium": "🟨 Medium",
    "High": "🟥 High"
}
df['RiskCategoryColored'] = df['RiskCategory'].map(color_map)

# ---------------------------
# Add Actionable Suggestions
# ---------------------------
def generate_suggestions(row):
    if row['RiskCategory'] == "High":
        return "🚨 Review resources & deadlines immediately"
    elif row['RiskCategory'] == "Medium":
        return "⚠️ Monitor progress closely"
    else:
        return "✅ On track"

df['Suggestion'] = df.apply(generate_suggestions, axis=1)

# ---------------------------
# Display Project Tasks Table
# ---------------------------
st.subheader("Project Tasks Overview")
st.dataframe(df[['TaskID','TaskName','RiskScore','RiskCategoryColored','Suggestion']])

# ---------------------------
# Display Critical Tasks Table
# ---------------------------
critical_tasks = df[df['Criticality']==1].sort_values(by='RiskScore', ascending=False)
critical_tasks['Suggestion'] = critical_tasks.apply(generate_suggestions, axis=1)

st.subheader("Critical Tasks")
st.dataframe(critical_tasks[['TaskID','TaskName','RiskScore','RiskCategoryColored','Suggestion']])

# ---------------------------
# Visualizations
# ---------------------------
st.subheader("Risk Heatmap")
st.pyplot(visuals.plot_heatmap(df))

st.subheader("Top-Risk Tasks")
st.pyplot(visuals.plot_top_risk_tasks(df, top_n=5))

# ---------------------------
# Project-Level Summary
# ---------------------------
st.subheader("Project Risk Summary")
st.metric("Max Task Risk", df['RiskScore'].max())
st.metric("Average Task Risk", round(df['RiskScore'].mean(), 2))

# ---------------------------
# Export CSV
# ---------------------------
st.subheader("Export Risk Report")
st.download_button(
    label="Download CSV",
    data=df.to_csv(index=False).encode('utf-8'),
    file_name='project_risk_report.csv',
    mime='text/csv'
)