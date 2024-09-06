FROM python:latest

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt && playwright install && playwright install-deps

#EXPOSE 8501
#EXPOSE #

# NOTE: `python main.py` command puts the server to sleep for 2 seconds before 
# running `pytest` in order to allow the other containers to build. Because this 
# container already requires up to 2 minutes to build, this command is probably
# unnecessary as the other containers should be up by the time the `pytest` command
# runs

# CMD ["python", "main.py"]
CMD ["pytest", "frontend"] #, "backend"]

