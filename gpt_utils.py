import os 
from langchain.prompts import ChatPromptTemplate 
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv 
load_dotenv()

os.environ['LANGSMITH_TRACING'] = 'true'
os.environ["LANGSMITH_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")
os.environ["OPENAI_API_KEY"]=os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(
    model = "gpt-4o-mini",
    temperature = 0.4
)

def explain_prediction(patient_data: dict, prediction: dict, user_query: str) -> str:
    template = """
        You are a clinical AI assistant. 
    A machine learning model has evaluated a patient.

    Patient Data:
    {patient_data}

    Model Output:
    Predictions: {predictions}
    Probabilities: {probabilities}

    The user has asked: "{user_query}"

    Please respond in a way that addresses the user query while covering:
    1. Explanation of the predictions
    2. Limitations or missing info
    3. Suggested follow-up actions
    4. Suggested medications or lifestyle changes based on demographics
    5. A disclaimer that this is not medical advice
    """

    prompt = ChatPromptTemplate.from_template(template)

    chain = prompt | llm 
    response = chain.invoke({
        "patient_data": patient_data,
        "predictions" : prediction.get("predictions"),
        "probabilities": prediction.get('probabilities'),
        "user_query": user_query,
    })

    return response.content