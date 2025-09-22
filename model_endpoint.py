from fastapi import FastAPI
from pydantic import BaseModel
from model_utils import *
from gpt_utils import explain_prediction

class InputData(BaseModel):
    data: dict        # patient features
    query: str        # user’s custom request

app = FastAPI(title="XGBoost + LangChain API")

@app.post("/predict")
def predict(input_data: InputData):
    try:
        # Run ML model
        prediction = run_model_e11(input_data.data)

        print(prediction)
        # Generate GPT explanation with user input
        gpt_output = explain_prediction(input_data.data, prediction, input_data.query)

        # Merge responses
        prediction["chatgpt_explanation"] = gpt_output
        return prediction

    except Exception as e:
        print(str(e))
        return {"error": str(e)}
