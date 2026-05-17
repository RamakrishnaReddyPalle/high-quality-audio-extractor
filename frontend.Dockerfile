FROM python:3.13-slim

RUN apt-get update && apt-get install -y \
    ffmpeg \
    curl \
    git \
    nodejs \
    npm \
    && apt-get clean

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD streamlit run frontend/streamlit_app.py --server.address 0.0.0.0 --server.port 8501