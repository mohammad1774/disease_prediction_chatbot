import pandas as pd
from joblib import load 

model = load('models/clf_xgb_final_e11.joblib')
feature_cols = load('models/feature_cols.joblib')

def run_model_e11(data: dict):

    df = pd.DataFrame([data])
    df = df.reindex(columns=feature_cols, fill_value=0)

    preds = model.predict(df)
    result = {"predictions": preds.tolist()}

    if hasattr(model, "predict_proba"):
        result["probabilities"] = model.predict_proba(df).tolist()

    return result

