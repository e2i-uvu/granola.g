FROM python:latest

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]
