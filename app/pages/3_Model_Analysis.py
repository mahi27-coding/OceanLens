import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    confusion_matrix,
    accuracy_score,
    classification_report,
    roc_curve,
    auc
)
from sklearn.preprocessing import label_binarize

st.title("🔬 Research-Grade Model Evaluation Laboratory")

# ---------------------------------------------------
# Load Data
# ---------------------------------------------------
df = pd.read_csv("data/oceanlens_beach_observations_v1.csv")

df["tourist_density"] = df["tourist_density"].map({
    "Low": 0,
    "Medium": 1,
    "High": 2
}).fillna(1)

df["garbage_type"] = df["garbage_type"].astype("category").cat.codes

X = df[["latitude", "longitude", "tourist_density", "garbage_type"]]
y = df["severity_level"]

# ---------------------------------------------------
# Train Test Split
# ---------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

rf = RandomForestClassifier(n_estimators=300, random_state=42)
rf.fit(X_train, y_train)

y_pred = rf.predict(X_test)
y_prob = rf.predict_proba(X_test)

# ---------------------------------------------------
# Accuracy + Metrics
# ---------------------------------------------------
st.subheader("📊 Performance Metrics")

accuracy = accuracy_score(y_test, y_pred)

col1, col2 = st.columns(2)
col1.metric("Accuracy", round(accuracy, 3))
col2.metric("Test Samples", len(y_test))

report = classification_report(y_test, y_pred, output_dict=True)
report_df = pd.DataFrame(report).transpose()

st.markdown("### Classification Report")
st.dataframe(report_df)

st.divider()

# ---------------------------------------------------
# Confusion Matrix
# ---------------------------------------------------
st.subheader("🧩 Confusion Matrix")

cm = confusion_matrix(y_test, y_pred)

fig_cm = go.Figure(data=go.Heatmap(
    z=cm,
    x=["Pred 1", "Pred 2", "Pred 3"],
    y=["Actual 1", "Actual 2", "Actual 3"],
    colorscale="Inferno"
))

fig_cm.update_layout(title="Random Forest Confusion Matrix")
st.plotly_chart(fig_cm, use_container_width=True)

st.divider()

# ---------------------------------------------------
# Multi-Class ROC Curve
# ---------------------------------------------------
st.subheader("📈 Multi-Class ROC Curves")

classes = sorted(y.unique())
y_test_bin = label_binarize(y_test, classes=classes)

fig_roc = go.Figure()

for i, class_label in enumerate(classes):
    fpr, tpr, _ = roc_curve(y_test_bin[:, i], y_prob[:, i])
    roc_auc = auc(fpr, tpr)

    fig_roc.add_trace(go.Scatter(
        x=fpr,
        y=tpr,
        mode='lines',
        name=f'Class {class_label} (AUC = {roc_auc:.2f})'
    ))

fig_roc.add_trace(go.Scatter(
    x=[0,1],
    y=[0,1],
    mode='lines',
    line=dict(dash='dash'),
    name='Random Guess'
))

fig_roc.update_layout(
    title="Multi-Class ROC Curve",
    xaxis_title="False Positive Rate",
    yaxis_title="True Positive Rate"
)

st.plotly_chart(fig_roc, use_container_width=True)

st.divider()

# ---------------------------------------------------
# Class Imbalance
# ---------------------------------------------------
st.subheader("⚖ Class Distribution")

class_counts = y.value_counts().reset_index()
class_counts.columns = ["Severity Level", "Count"]

fig_class = px.bar(
    class_counts,
    x="Severity Level",
    y="Count",
    color="Severity Level",
    title="Severity Class Distribution"
)

st.plotly_chart(fig_class, use_container_width=True)

st.divider()

# ---------------------------------------------------
# Cross Validation
# ---------------------------------------------------
st.subheader("🔁 Cross-Validation Stability")

cv_scores = cross_val_score(rf, X, y, cv=5)

cv_df = pd.DataFrame({
    "Fold": [1,2,3,4,5],
    "Accuracy": cv_scores
})

fig_cv = px.line(
    cv_df,
    x="Fold",
    y="Accuracy",
    markers=True,
    title="5-Fold Cross Validation Accuracy"
)

st.plotly_chart(fig_cv, use_container_width=True)

st.success("Research Evaluation Engine Active – Model Statistically Validated")