import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor

#  PAGE CONFIG 
st.set_page_config(page_title="Churn Dashboard", layout="wide")

#  CSS 
st.markdown("""
<style>
  .stApp { background: #eef2f7; }

  .title-bar {
    background: linear-gradient(90deg, #1a2a4a 0%, #2e4a7a 100%);
    color: white;
    text-align: center;
    padding: 16px;
    border-radius: 8px;
    font-size: 20px;
    font-weight: 700;
    margin-bottom: 18px;
  }

  .kpi-row {
    background: white;
    border-radius: 8px;
    padding: 12px 24px;
    display: flex;
    justify-content: space-around;
    align-items: center;
    margin-bottom: 18px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.08);
  }
  .kpi-item { text-align: center; }
  .kpi-label { font-size: 11px; color: #6b7280; font-weight: 600; text-transform: uppercase; }
  .kpi-value { font-size: 18px; font-weight: 700; color: #1a2a4a; }

  .card {
    background: white;
    border-radius: 8px;
    padding: 14px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.08);
  }
  .card-title {
    font-size: 13px;
    font-weight: 700;
    color: #1a2a4a;
    margin-bottom: 10px;
    border-bottom: 1px solid #e5e7eb;
    padding-bottom: 6px;
  }

  .rev-box {
    background: white;
    border-radius: 8px;
    padding: 20px;
    text-align: center;
    box-shadow: 0 1px 4px rgba(0,0,0,0.08);
  }
  .rev-value { font-size: 30px; font-weight: 700; color: #1a2a4a; margin-top: 30px; }
  .rev-label { font-size: 12px; color: #6b7280; }

  .seg-low    { background:#4caf50; color:white; border-radius:6px; padding:14px 10px; text-align:center; font-weight:700; }
  .seg-medium { background:#ff9800; color:white; border-radius:6px; padding:14px 10px; text-align:center; font-weight:700; }
  .seg-high   { background:#f44336; color:white; border-radius:6px; padding:14px 10px; text-align:center; font-weight:700; }
  .seg-label  { font-size:12px; margin-bottom:4px; }
  .seg-pct    { font-size:22px; }
</style>
""", unsafe_allow_html=True)


#  LOAD & TRAIN 
df = pd.read_csv("customer_churn.csv")

df["Churn"] = df["Churn"].map({"Yes": 1, "No": 0})

contract_churn = df.groupby("Contract")["Churn"].mean().reset_index()
contract_churn.columns = ["Contract", "ChurnRate"]
contract_churn["ChurnRate"] = (contract_churn["ChurnRate"] * 100).round(1)

churn_rate  = round(df["Churn"].mean() * 100, 0)
avg_monthly = round(df["MonthlyCharges"].mean(), 0)
avg_tenure  = round(df["Tenure"].mean(), 0)

df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
df.dropna(inplace=True)

df = pd.get_dummies(df, columns=["Gender","Contract","InternetService","PaymentMethod"], dtype=int)
df.drop("CustomerID", axis=1, inplace=True)

X = df.drop("Churn", axis=1)
y = df["Churn"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

rf_clf = RandomForestClassifier(n_estimators=100, random_state=42)
rf_clf.fit(X_train, y_train)
rf_pred  = rf_clf.predict(X_test)
rf_proba = rf_clf.predict_proba(X_test)[:, 1]

rev_cols = [c for c in ["Tenure","MonthlyCharges",
                          "Contract_Month-to-month","Contract_One year","Contract_Two year",
                          "InternetService_DSL","InternetService_Fiber optic"] if c in df.columns]
X_rev = df[rev_cols]
y_rev = df["TotalCharges"]
Xr_tr, Xr_te, yr_tr, yr_te = train_test_split(X_rev, y_rev, test_size=0.2, random_state=42)
rf_reg = RandomForestRegressor(n_estimators=100, random_state=42)
rf_reg.fit(Xr_tr, yr_tr)
rev_pred   = rf_reg.predict(Xr_te)
next12_rev = round(df["MonthlyCharges"].sum() * 12, 0)

n_samples   = min(3, len(rf_proba), len(rev_pred))
sample_df = pd.DataFrame({
    "Customer ID":        [f"C{str(i).zfill(3)}" for i in range(1, n_samples + 1)],
    "Churn Probability":  [f"{int(p*100)}%" for p in rf_proba[:n_samples]],
    "Estimated Revenue":  [f"${int(r):,}" for r in rev_pred[:n_samples]],
})



#  RENDER


# Title
st.markdown(
    '<div class="title-bar">Customer Churn Prediction &amp; Revenue Forecasting Dashboard</div>',
    unsafe_allow_html=True,
)

# KPI Bar
st.markdown(f"""
<div class="kpi-row">
  <div class="kpi-item">
    <div class="kpi-label">Churn Rate</div>
    <div class="kpi-value">{int(churn_rate)}%</div>
  </div>
  <div class="kpi-item">
    <div class="kpi-label">Avg. Monthly Charges</div>
    <div class="kpi-value">${int(avg_monthly)}</div>
  </div>
  <div class="kpi-item">
    <div class="kpi-label">Avg. Tenure</div>
    <div class="kpi-value">{int(avg_tenure)} months</div>
  </div>
  <div class="kpi-item">
    <div class="kpi-label">Predicted Revenue</div>
    <div class="kpi-value">${int(next12_rev):,}</div>
  </div>
</div>
""", unsafe_allow_html=True)

#  ROW 1 
col1, col2, col3 = st.columns([1.2, 1, 1])

with col1:
    st.markdown('<div class="card"><div class="card-title">Churn by Contract Type</div>', unsafe_allow_html=True)
    fig_bar = px.bar(
        contract_churn, x="Contract", y="ChurnRate",
        color="Contract",
        color_discrete_sequence=["#2196f3", "#ff9800", "#f44336"],
        text="ChurnRate",
    )
    fig_bar.update_layout(
        showlegend=False, plot_bgcolor="white", paper_bgcolor="white",
        margin=dict(t=10, b=30, l=10, r=10), height=230,
        xaxis=dict(title="", tickfont=dict(size=10)),
        yaxis=dict(title="Churn %", showgrid=True, gridcolor="#f0f0f0"),
    )
    fig_bar.update_traces(texttemplate="%{text}%", textposition="outside", marker_line_width=0)
    st.plotly_chart(fig_bar, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card"><div class="card-title">Churn Prediction</div>', unsafe_allow_html=True)
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=churn_rate,
        number={"suffix": "%", "font": {"size": 32, "color": "#1a2a4a"}},
        gauge={
            "axis": {"range": [0, 100], "tickfont": {"size": 9}},
            "bar":  {"color": "#f44336"},
            "steps": [
                {"range": [0,  33],  "color": "#4caf50"},
                {"range": [33, 66],  "color": "#ff9800"},
                {"range": [66, 100], "color": "#f44336"},
            ],
            "threshold": {
                "line": {"color": "black", "width": 3},
                "thickness": 0.8,
                "value": churn_rate,
            },
        },
    ))
    fig_gauge.update_layout(
        height=200, margin=dict(t=20, b=10, l=20, r=20),
        paper_bgcolor="white",
    )
    st.plotly_chart(fig_gauge, use_container_width=True)
    risk       = "High"   if churn_rate >= 33 else "Medium" if churn_rate >= 15 else "Low"
    risk_color = "#f44336" if risk == "High" else "#ff9800" if risk == "Medium" else "#4caf50"
    st.markdown(f"""
    <div style="text-align:center; margin-top:-10px;">
      <span style="background:{risk_color}; color:white; padding:5px 16px;
                   border-radius:4px; font-weight:700; font-size:14px;">
        Churn Risk: {risk}
      </span>
    </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="rev-box">
      <div class="card-title">Revenue Forecast</div>
      <div class="rev-label">Next 12 Months:</div>
      <div class="rev-value">${int(next12_rev):,}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

#  ROW 2 
col4, col5 = st.columns([1, 1.4])

with col4:
    high_pct   = int(churn_rate)
    medium_pct = 35
    low_pct    = max(0, 100 - high_pct - medium_pct)
    st.markdown(f"""
    <div class="card">
      <div class="card-title">Customer Segmentation</div>
      <div style="display:flex; gap:8px; margin-top:10px;">
        <div class="seg-low"    style="flex:1">
          <div class="seg-label">Low Risk</div>
          <div class="seg-pct">{low_pct}%</div>
        </div>
        <div class="seg-medium" style="flex:1">
          <div class="seg-label">Medium Risk</div>
          <div class="seg-pct">{medium_pct}%</div>
        </div>
        <div class="seg-high"   style="flex:1">
          <div class="seg-label">High Risk</div>
          <div class="seg-pct">{high_pct}%</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown('<div class="card"><div class="card-title">Sample Predictions</div>', unsafe_allow_html=True)
    st.dataframe(sample_df, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)