FROM python:latest

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt && playwright install && playwright install-deps

#EXPOSE 8501
#EXPOSE #

CMD ["python", "main.py"]

