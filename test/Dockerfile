FROM python:latest

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt && playwright install

#EXPOSE 8501
#EXPOSE #

CMD ["python", "main.py"]

