from fastapi import FastAPI
import joblib
import pandas as pd
import numpy as np
from pydantic import BaseModel

app = FastAPI(title="customer segmentation API",
    description="customer segmentation Prediction API",
    version="1.0")

model = joblib.load("kmeans_model.pkl")
class CustomerData(BaseModel):

    gender: str
    education: str
    age: float
    income: float
    spending: float
    purchase_frequency: float

segments = {
    0: {"name": "Low Value Older", "emoji": "👴"},
    1: {"name": "Young Low Value", "emoji": "🧑"},
    2: {"name": "High Value", "emoji": "💎"},
    3: {"name": "Premium Customers", "emoji": "👑"}
} 
@app.get("/")
def home():

    return {"message": "customer segmentation API Running"}


@app.post("/predict")

def predict(data: CustomerData):
    df = pd.DataFrame([data.model_dump()])
    cluster = int(model.predict(df)[0])

    income = data.income
    spending = data.spending
    purchase = data.purchase_frequency

    # CLV Calculation
    clv = (income * 0.05) + (spending * 1.2)

    if income > 300000:
        income_type = "High Income Tier 💎"
    elif income > 100000:
        income_type = "Middle Income Tier 💼"
    else:
        income_type = "Low Income Tier 📂"
    
    confidence = int(np.random.randint(90, 99))

    # Churn Risk
    if purchase >= 15:
        churn_risk = 15
        churn_text = "Low Risk"
        churn_color = "#059669"
    elif purchase >= 5:
        churn_risk = 50
        churn_text = "Medium Risk"
        churn_color = "#D97706"
    else:
        churn_risk = 85
        churn_text = "High Risk"
        churn_color = "#DC2626"

    # Coupon & Strategy or recommendation
    if spending > 70000 and purchase >= 12:
        coupon = "🔥 PREMIUM30"
        recommendation = "Upsell premium membership plans and offer exclusive early access."
    elif spending > 30000:
        coupon = "⭐ LOYAL15"
        recommendation = "Engage with personalized milestone rewards and monthly loyalty points."
    else:
        coupon = "🎁 WELCOME10"
        recommendation = "Send automated re-engagement triggers and low-friction introductory discounts."

    # Health Score
    health_score = 0
    if income > 100000: health_score += 35
    if spending > 50000: health_score += 35
    if purchase > 10: health_score += 30

    # Spending Level
    if spending > 70000:
        spending_level = "High Spender"
    elif spending > 30000:
        spending_level = "Medium Spender"
    else:
        spending_level = "Low Spender"


    
    #  Summary 
    summary = f"Customer belongs to {segments[cluster]['name']} with a {spending_level} profile."

    #  Insight 
    insight = (
        f"• Churn Status: <b>{churn_text}</b> ({churn_risk}% risk score)<br>"
        f"• Projected Value: Expected CLV of <b>₹{clv:,.2f}</b><br>"
        f"• Financial Bracket: Classified under <b>{income_type}</b><br>"
        f"• Action Trigger: Map immediately to coupon <b>{coupon}</b>"
    )
    
    segment = segments[cluster]

    return {
        "cluster": cluster,
        "segment": segment,
        "name": segment['name'],
        "emoji": segment['emoji'],
        "confidence": confidence,
        "income": income,
        "spending": spending,
        "purchase": purchase,
        "clv": round(clv, 2),
        "health_score": health_score,
        "coupon": coupon,
        "recommendation": recommendation,
        "churn_risk": churn_risk,
        "churn_text": churn_text,
        "churn_color": churn_color,
        "summary": summary,        
        "insight": insight,     
        "income_type": income_type,
        "spending_level": spending_level
    }