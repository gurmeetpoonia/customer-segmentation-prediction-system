
import streamlit as st 
import pandas as pd
import numpy as np
from datetime import date
import requests
if "payload" in st.session_state and "restored" not in st.session_state:

    old = st.session_state.payload

    for k,v in old.items():
        st.session_state[k] = v

    st.session_state.restored = True

if "reset_form" in st.session_state and st.session_state.reset_form:

    st.session_state.gender = "Select"
    st.session_state.education = "Select"
    st.session_state.age = 0
    st.session_state.income = 0
    st.session_state.spending = 0
    st.session_state.purchase_frequency = 0

    st.session_state.reset_form = False

st.markdown("""
<style>

/* Sidebar hide */
[data-testid="stSidebar"] {
    display: none;
}

/* Sidebar toggle button hide */
[data-testid="stSidebarCollapsedControl"] {
    display: none;
}

/* Header hide (optional) */
[data-testid="stHeader"] {
    display: none;
}

</style>
""", unsafe_allow_html=True)

st.title("💎 Customer Segmentation")

gender = st.selectbox("Gender", ["Select","Male", "Female"],key="gender")
education = st.selectbox("Education", ["Select","High School", "Graduate", "Post Graduate"],key="education")

age=st.number_input("Age",step=1,key="age")
income = st.number_input("Income",min_value=0,key="income")
spending = st.number_input("Spending",min_value=0, step=1000,key="spending")
purchase = st.number_input("Purchase Frequency",min_value=0,key="purchase_frequency")
col1, col2 = st.columns(2)


with col1:
    predict = st.button("🚀 Predict Segment",
                        width="stretch")

with col2:
    reset = st.button("🔄 Reset Form",
                      width="stretch")

if reset:

    st.session_state.reset_form = True

    st.rerun()

    
    
if predict:
    if gender=="Select" or education=="Select" or age== 0 or income== 0 or spending== 0 or  purchase== 0:
        st.toast("Please fill all required field")
        st.stop ()


    payload={

        "age":int(age),

        "income":float(income),

        "spending":float(spending),

        "purchase_frequency":float(purchase),

        "gender":gender,

        "education":education

    }

    try:
        st.session_state.payload=payload
        response=requests.post(

        "https://customer-segmentation-prediction-system.onrender.com/predict",

        json=payload

    )



        result=response.json()


        st.session_state.result=result


        st.switch_page("pages/analysis.py")
        st.write(st.session_state)

    except(Exception):
            st.error("⚠️ API is not running.")
            st.stop()