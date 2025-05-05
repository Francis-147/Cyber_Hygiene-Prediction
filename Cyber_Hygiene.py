import streamlit as st
import pandas as pd
import numpy as np
import json
import pickle

 
with open('data_columns.json', 'r') as f:
         data_columns = json.load(f)['data_columns']

model = pickle.load(open('model.pickle', 'rb'))

def predict(sex, age_range, educational_level, academic_status, training_on_internet_security, use_of_antivirus,
       min_num_password, performance_of_run_scan_operation_on_your_devices, meaning_of_cyberhygiene, 
        virus_cant_enter_a_device_through):
    
    X = pd.DataFrame(columns=data_columns)
    # Create input array with zeros
    Y = np.zeros(len(X.columns))

    # Assign numerical values to respective positions
    features = {
            "Sex": np.where(X.columns == sex)[0][0],
            "Age_Range": np.where(X.columns == age_range)[0][0],
            "Educational_Level": np.where(X.columns == educational_level)[0][0],
            "Academic_Status": np.where(X.columns == academic_status)[0][0],
            "Training_on_Internet_Security": np.where(X.columns == training_on_internet_security)[0][0],
            "Use_of_Antivirus": np.where(X.columns == use_of_antivirus)[0][0], 
            "Min_num_in_Password": np.where(X.columns == min_num_password)[0][0],
            "Performance_of_Run_Scan_Operation_on_Your_Devices": np.where(X.columns == performance_of_run_scan_operation_on_your_devices)[0][0],
            "Meaning_of_Cyberhygiene": np.where(X.columns == meaning_of_cyberhygiene)[0][0], 
            "Virus_Cant_Enter_a_Device_Through" : np.where(X.columns == virus_cant_enter_a_device_through)[0][0], 
      }

    
    for feature, value in features.items():
        if value >= 0:
            Y[value] = 1

    
    return (model.predict_proba([Y]))[0][1]


# Streamlit UI
st.set_page_config(page_title="Cyber Hygiene Checker")

import base64

def set_bg_from_local(image_file):
    with open(image_file, "rb") as file:
        encoded = base64.b64encode(file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-attachment: fixed;
        }}
        h1, h2, h3, h4, h5, h6, p,  label {{
            color: #ffffff !important;
         }}

        
        div.stButton > button {{
            background-color: #1f77b4;
            color: white;
            border-radius: 10px;
            padding: 12px 24px;
            font-size: 18px;
            font-weight: bold;
            border: none;
            cursor: pointer;
        }}

        div.stButton > button:hover {{
            background-color: #105a8b;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


set_bg_from_local("img-3.jpg")

st.title("🛡️ Cyber Hygiene Prediction")
st.markdown("Use this to evaluate your cyber hygiene practices.")

st.markdown("---")
col1, spacer, col2 = st.columns([1, 0.2, 1]) 

# User input
with col1:
    sex = st.selectbox("What is your sex ?", [
        'A. Male', 'Female'
    ])

    age_range = st.selectbox("What is your age range ?", [
        'A. 15-24 years', 'B. 25-34 years','C. 35-44 years', 'D. 45-54 years','E.  Above 54 years'
    ])

    education = st.selectbox("What is your educational level ?", [
        'C. Diploma', 'D. Undergraduate', 'E. Graduate', 'F. Masters', 'G. Doctorate'
    ])

    status = st.selectbox("What is your academic status ?", [
        'A. Student', 'B. Academic Staff', 'C. Non-academic Staff'
    ])

    training = st.selectbox("Have you had training on internet security ?", [
        'A. Yes', 'B. No'
    ])
    antivirus = st.selectbox("When do you use antivirus on your devices ?", [
        'A. Every time', 'B. Often', 'C. Rarely', 'D. Never'
    ])

with col2:

    min_password = st.selectbox("The minimum number of characters a strong password should contain is:", [
        'A. Six','B. Four', 'C. Eight', 'D. Five'
    ])

    scan_freq = st.selectbox("How often do you run scan operations on your devices ?", [
        'A. Every time', 'B. Often', 'C. Rarely', 'D. Never'
    ])

    hygiene_meaning = st.selectbox("What is the meaning of Cyber Hygiene ?", [
        'A. Use of antispyware', 'B. Frequent formatting of hard disk','C. Running antivirus scan at least once a week',
        'D. It is those practices an internet user should engage in to avoid cyber attack'
    ])

    virus_entry = st.selectbox("A virus can't enter a device through:", [
        'A. Software update', 'B. The use of infected device', 'C. Downloading from unsecured sites',
        'D. The use of unprotected devices'
    ])

# Prediction
st.markdown("---")

if st.button("🔍 Check My Cyber Hygiene Status"):
    prediction = predict(sex, age_range, education, status, training, antivirus, min_password, scan_freq, hygiene_meaning, virus_entry)
    
    st.subheader(f"Result: **{round(prediction * 100, 1)}%** of good cyber hygiene practice")
    
    if prediction >= 0.5:
        st.success("✅ You likely have good cyber hygiene.")
    else:
        st.warning("⚠️ Your cyber hygiene may need improvement.")


