import streamlit as st
import pandas as pd
import requests
from dotenv import load_dotenv
import os
load_dotenv()

ENDPOINT_URL = os.getenv("ENDPOINT_URL")

# ------------------------
# Training Feature Groups
# ------------------------
lab_cols = ['50931']

demographics_cont_cols = ['bmi','weight','height_filled']

diabetes_meds = [
    'acarbose','apidra','bydureon','byetta','humalog','insulin_degludec',
    'insulin_detemir','insulin_glargine','insulin_glulisine','insulin_lispro',
    'insulin_regular','invokana','janumet','januvia','jardiance','jentadueto',
    'lantus','levemir','linagliptin','liraglutide','metformin','nateglinide',
    'novolog','ozempic','pioglitazone','repaglinide','semaglutide','sitagliptin',
    'tradjenta','tresiba','trulicity','victoza','canagliflozin','dapagliflozin',
    'empagliflozin','farxiga'
]

antihypertensives = [
    'amlodipine','atenolol','avapro','benazepril','bisoprolol','bumetanide',
    'bystolic','candesartan','captopril','carvedilol','clonidine','coreg',
    'diovan','diltiazem','enalapril','hydralazine','hydrochlorothiazide',
    'indapamide','irbesartan','isosorbide_dinitrate','isosorbide_mononitrate',
    'ivabradine','labetalol','lisinopril','losartan','methyldopa','metoprolol',
    'minoxidil','nebivolol','nifedipine','nitroglycerin','olmesartan','ramipril',
    'sacubitril_valsartan','spironolactone','torsemide','valsartan','verapamil',
    'furosemide'
]

statins = ['atorvastatin','lovastatin','pravastatin','rosuvastatin','simvastatin']

antiplatelets_anticoagulants = [
    'amiodarone','apixaban','aspirin','clopidogrel','coumadin','digoxin',
    'dipyridamole','dofetilide','enoxaparin','entresto','felodipine','heparin',
    'plavix','prasugrel','ranolazine','rivaroxaban','ticagrelor','warfarin',
    'xarelto'
]

meds_cat_cols = (
    diabetes_meds + antihypertensives + statins + antiplatelets_anticoagulants
)

demographics_cat_cols = [
    'race_american_indian_alaska_native','race_asian','race_asian_asian_indian',
    'race_asian_chinese','race_asian_korean','race_asian_south_east_asian',
    'race_black_african','race_black_african_american','race_black_cape_verdean',
    'race_black_caribbean_island','race_hispanic_or_latino',
    'race_hispanic_latino_central_american','race_hispanic_latino_columbian',
    'race_hispanic_latino_cuban','race_hispanic_latino_dominican',
    'race_hispanic_latino_guatemalan','race_hispanic_latino_honduran',
    'race_hispanic_latino_mexican','race_hispanic_latino_puerto_rican',
    'race_hispanic_latino_salvadoran','race_multiple_race_ethnicity',
    'race_native_hawaiian_or_other_pacific_islander','race_other',
    'race_patient_declined_to_answer','race_portuguese','race_south_american',
    'race_unable_to_obtain','race_unknown','race_white','race_white_brazilian',
    'race_white_eastern_european','race_white_other_european','race_white_russian',
    'ms_divorced','ms_married','ms_single','ms_widowed',
    'lang_american_sign_language','lang_amharic','lang_arabic','lang_armenian',
    'lang_bengali','lang_chinese','lang_english','lang_french','lang_haitian',
    'lang_hindi','lang_italian','lang_japanese','lang_kabuverdianu','lang_khmer',
    'lang_korean','lang_modern_greek_1453','lang_other','lang_persian','lang_polish',
    'lang_portuguese','lang_russian','lang_somali','lang_spanish','lang_thai',
    'lang_vietnamese','F','M','delta_age'
]

feature_cols = lab_cols + meds_cat_cols + demographics_cat_cols + demographics_cont_cols

# ------------------------
# Streamlit Form
# ------------------------
st.set_page_config(page_title="Medical Data Input", page_icon="🩺", layout="wide")
st.title("🩺 Project Data Collection Form")

with st.form("medical_form"):
    st.header("Concern")
    query = st.text_input('Ask your Medical Concern')

    st.header("📊 Demographics (Continuous)")
    bmi = st.number_input("BMI", min_value=0.0, step=0.1)
    weight = st.number_input("Weight (kg)", min_value=0.0, step=0.1)
    height = st.number_input("Height (cm)", min_value=0.0, step=0.1)
    delta_age = st.number_input("Delta Age", min_value=0, step=1)

    st.header("🌍 Demographics (Categorical)")
    race = st.selectbox("Race", demographics_cat_cols[:20])
    language = st.selectbox("Language", demographics_cat_cols[40:60])
    marital_status = st.selectbox("Marital Status", ["ms_single","ms_married","ms_divorced","ms_widowed"])
    gender = st.selectbox("Gender", ["M", "F"])

    st.header("🧪 Lab Tests")
    lab_50931 = st.number_input("Lab Test 50931", min_value=0.0, step=0.1)

    st.header("💊 Medications — Diabetes")
    diabetes_inputs = {med: st.checkbox(med, value=False) for med in diabetes_meds}

    st.header("💊 Medications — Antihypertensives")
    antiht_inputs = {med: st.checkbox(med, value=False) for med in antihypertensives}

    st.header("💊 Medications — Statins")
    statin_inputs = {med: st.checkbox(med, value=False) for med in statins}

    st.header("💊 Medications — Antiplatelets / Anticoagulants")
    anti_platelet_inputs = {med: st.checkbox(med, value=False) for med in antiplatelets_anticoagulants}

    submitted = st.form_submit_button("✅ Submit")

if submitted:
    st.success("Form submitted successfully!")

    # Build user_data aligned with feature_cols
    user_data = {col: 0 for col in feature_cols}  # init all to 0

    # Fill in demographics continuous
    user_data["bmi"] = bmi
    user_data["weight"] = weight
    user_data["height_filled"] = height
    user_data["delta_age"] = delta_age

    # Fill in categorical (set selected to 1)
    user_data[race] = 1
    user_data[language] = 1
    user_data[marital_status] = 1
    user_data[gender] = 1

    # Lab
    user_data["50931"] = lab_50931

    # Meds
    for med_dict in [diabetes_inputs, antiht_inputs, statin_inputs, anti_platelet_inputs]:
        for med, val in med_dict.items():
            user_data[med] = int(val)

    # Show
    # st.write("### 📝 Model-ready Data (aligned with training)")
    # st.json(user_data)

    # Send to API
    api_url = "{ENDPOINT_URL}/predict"
    response = requests.post(api_url, json={"data": user_data,"query": query})

    if response.status_code == 200:
        response_json = response.json()

        st.header("🔮 Model Predictions & Probabilities")
        preds = response_json.get("predictions", [])
        probs = response_json.get("probabilities", [])

        if probs:
            df_results = pd.DataFrame(probs, columns=[f"Class {i}" for i in range(len(probs[0]))])
            df_results.insert(0, "Prediction", preds)
            st.table(df_results)
        else:
            st.write("Predictions:", preds)

        st.header("💬 ChatGPT Explanation")
        explanation = response_json.get("chatgpt_explanation", "No explanation available")
        st.write(explanation)

    else:
        st.error(f"API Error: {response.status_code} | {response.text}")
