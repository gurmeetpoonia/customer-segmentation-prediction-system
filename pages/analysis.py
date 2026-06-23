import streamlit as st 
import numpy as np 
import plotly.graph_objects as go
if "result" not in st.session_state:
    st.warning("Please predict a customer segment first.")
    if st.button("⬅ Back to Prediction"):
        st.switch_page("streamlit_app.py")
    st.stop()

result = st.session_state.result

# 💎 Page Config
st.set_page_config(
    page_title="Customer Segmentation",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- ADVANCED CSS STYLING ---
st.markdown("""
<style>
[data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"], [data-testid="stHeader"] {
    display: none !important;
}
.main .block-container {
    padding-left: 5rem !important;
    padding-right: 5rem !important;
}
.card-3d {
    padding: 25px; border-radius: 20px; background: #ffffff;
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05), 0 20px 40px -5px rgba(0, 0, 0, 0.03);
    margin-bottom: 25px; border: 1px solid rgba(0, 0, 0, 0.04);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.card-3d:hover {
    transform: translateY(-5px);
    box-shadow: 0 20px 35px -5px rgba(0, 0, 0, 0.1), 0 30px 50px -10px rgba(0, 0, 0, 0.07);
}
.result-3d { background: linear-gradient(135deg, #1E40AF, #6D28D9); color: white; }
.insight-3d { border-top: 5px solid #2563EB; background: linear-gradient(to bottom right, #FFFFFF, #F0F6FF); }
.recommend-3d { border-top: 5px solid #D97706; background: linear-gradient(to bottom right, #FFFFFF, #FEFBF0); }
.analysis-3d { border-top: 5px solid #059669; background: linear-gradient(to bottom right, #FFFFFF, #ECFDF5); }
.feature-card { border-top: 5px solid #EC4899; background: linear-gradient(to bottom right, #FFFFFF, #FDF2F8); } 
.health-card { border-top: 5px solid #10B981; background: linear-gradient(to bottom right, #FFFFFF, #F0FDF4); }

.metric-3d {
    background: #ffffff; padding: 20px; border-radius: 16px; text-align: center;
    box-shadow: 0 8px 20px rgba(0,0,0,0.04); border: 1px solid #F3F4F6;
}
.metric-label { font-size: 0.85rem; color: #6B7280; font-weight: 600; text-transform: uppercase; }
.metric-val { font-size: 1.8rem; color: #111827; font-weight: 800; margin-top: 5px; }
.progress-bg { background: #E5E7EB; border-radius: 10px; height: 12px; width: 100%; margin-top: 8px; overflow: hidden; }
.progress-fill { height: 100%; border-radius: 10px; }
.badge { padding: 4px 10px; border-radius: 8px; font-weight: bold; font-size: 0.9rem; display: inline-block; }
</style>
""", unsafe_allow_html=True)


# Extract Variables Safely
cluster = result["cluster"]
emoji = result["emoji"]
confidence = result["confidence"]
income = result["income"]
spending = result["spending"]
purchase = result["purchase"]
health_score = result["health_score"]
coupon = result["coupon"]
recommendation = result.get("recommendation", "N/A")

# --- FETCHING SEPARATED FIELDS ---
summary = result.get("summary", "No Summary Available")
insight = result.get("insight", "No Insight Available")

clv_predicted = result["clv"]
churn_risk = result["churn_risk"]
churn_text = result["churn_text"]
churn_color = result["churn_color"]
income_type = result["income_type"]
spending_level = result["spending_level"]

st.title("📊 Advanced Customer Intelligence Dashboard")
st.write("---")

# Hero Card
left_spacer, center_card, right_spacer = st.columns([1, 2, 1])
with center_card:
    st.markdown(f"""
    <div class='card-3d result-3d' style='margin-top: 15px;'>
        <h1 style='text-align:center; margin:0; font-size:3rem;'>{emoji}</h1>
        <h2 style='text-align:center; margin:5px 0; font-weight:700; font-size:1.8rem;'>{result['name']}</h2>
        <p style='text-align:center; margin:0; font-weight:500; font-size:1rem;'>
            Assigned Cluster Profile: <span style='background: rgba(255,255,255,0.2); padding: 2px 8px; border-radius: 6px;'><b>{cluster}</b></span>
           <span class='badge' style='background: rgba(255,255,255,0.2);'>Confidence: {confidence}%</span> 
        </p>
    </div>
    """, unsafe_allow_html=True)

# Metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"<div class='metric-3d'><div class='metric-label'>💰 Annual Income</div><div class='metric-val'>₹{income:,.0f}</div></div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div class='metric-3d'><div class='metric-label'>💳 Spending Amount</div><div class='metric-val'>₹{spending:,.0f}</div></div>", unsafe_allow_html=True)
with col3:
    st.markdown(f"<div class='metric-3d'><div class='metric-label'>🛒 Total Purchases</div><div class='metric-val'>{purchase}</div></div>", unsafe_allow_html=True)

st.write("") 

# Core Analytics (Insight & Recommendation)
st.write("### 🔑 Core Segment Analytics")
layout_col1, layout_col2 = st.columns(2)

with layout_col1:
    st.markdown(f"""
    <div class='card-3d insight-3d' style='height: 100%; min-height: 160px;'>
        <h3 style='color: #1E40AF; margin-bottom:12px; font-weight:700;'>💡 Customer Insight</h3>
        <p style='color: #1E3A8A; line-height: 1.6;'>{insight}</p>
    </div>
    """, unsafe_allow_html=True)

with layout_col2:
    st.markdown(f"""
    <div class='card-3d recommend-3d' style='height: 100%; min-height: 160px;'>
        <h3 style='color: #92400E; margin-bottom:12px; font-weight:700;'>🎯 Strategic Recommendation</h3>
        <p style='color: #78350F; line-height: 1.6;'>{recommendation}</p>
    </div>
    """, unsafe_allow_html=True)

# Health Score
st.markdown(f"""
<div class='card-3d health-card'>
    <div style='display: flex; justify-content: space-between; align-items: center;'>
        <h3 style='color:#065F46; margin: 0;'>⭐ Customer Health Score</h3>
        <span style='font-size: 1.5rem; font-weight: 800; color: #065F46;'>{health_score}/100</span>
    </div>
    <div class='progress-bg' style='height: 16px; background: #D1FAE5; margin-top: 15px;'>
        <div class='progress-fill' style='width: {health_score}%; background: linear-gradient(90deg, #10B981, #059669);'></div>
    </div>
</div>
""", unsafe_allow_html=True)

# Matrices Block
st.write("### ⚡ AI-Driven Behavior & Predictive Matrix")
feat_col1, feat_col2 = st.columns(2)

with feat_col1:
    st.markdown(f"""
    <div class='card-3d analysis-3d' style='margin-bottom:20px;'>
        <h3 style='color: #065F46; font-weight:700;'>📈 Spending & Financial Profile</h3>
        <p style='color: #065F46;'>💰 <b>Financial Status:</b> {income_type}</p>
        <p style='color: #065F46;'>💳 <b>Behavior Tag:</b> {spending_level}</p>
        <p style='color: #065F46;'>🛍️ <b>Purchase Frequency:</b> {purchase} Orders Processed</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class='card-3d feature-card'>
        <h3 style='color: #BE185D; font-weight:700;'>🎟️ Automated Target Campaign</h3>
        <div style='margin-top:12px;'><span class='badge' style='background: #FCE7F3; color: #DB2777; border: 1px dashed #EC4899; font-size:1.1rem; padding: 8px 15px;'>{coupon}</span></div>
    </div>
    """, unsafe_allow_html=True)

with feat_col2:
    st.markdown(f"""
    <div class='card-3d feature-card' style='margin-bottom:20px;'>
        <h3 style='color: #BE185D; font-weight:700;'>🔮 Customer Lifetime Value (CLV)</h3>
        <h2 style='color: #EC4899; margin-top: 10px; font-weight: 800;'>₹{clv_predicted:,.2f}</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class='card-3d feature-card'>
        <h3 style='color: #BE185D; font-weight:700;'>⚠️ Churn Risk Assessment</h3>
        <b style='color: {churn_color}; font-size: 1.1rem;'>{churn_text} ({churn_risk}%)</b>
        <div class='progress-bg'><div class='progress-fill' style='width: {churn_risk}%; background: {churn_color};'></div></div>
    </div>
    """, unsafe_allow_html=True)

st.write("---")

# --- AI EXECUTIVE SUMMARY (Now displays separated summary) ---
st.markdown(f"""
<div class='card-3d feature-card'>
    <h3 style='color:#BE185D; margin-top: 0;'>🤖 AI Executive Summary</h3>
    <div style='line-height:2; font-size:16px; color: #4D0A2A;'>
        {summary}
    </div>
</div>
""", unsafe_allow_html=True)

# Radar Chart
st.write("### 📊 Customer Behavior Radar Chart")
income_score = min(income/300000*100, 100)
spending_score = min(spending/100000*100, 100)
purchase_score = min(purchase/20*100, 100)
clv_score = min(clv_predicted/200000*100, 100)
loyalty_score = 100 - churn_risk

categories = ['Income', 'Spending', 'Purchase', 'CLV', 'Loyalty', 'Income']
values = [income_score, spending_score, purchase_score, clv_score, loyalty_score, income_score]

fig = go.Figure()
fig.add_trace(go.Scatterpolar(r=values, theta=categories, fill='toself', line=dict(color='#6D28D9')))
fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=False, height=450, margin=dict(t=20, b=20, l=20, r=20))
st.plotly_chart(fig, width="stretch")
if st.button("⬅ Back to Prediction"):
    st.switch_page("streamlit_app.py")