FROM python:3.13-slim 

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \ 
    gcc \
    && rm -rf /var/lib/apt/lists/* 

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt 

COPY . . 

EXPOSE 8000 8001


CMD bash -c "uvicorn model_endpoint:app --host 0.0.0.0 --port 8000 & \
            streamlit run app.py --server.port=8001"