FROM python:3.10.6

RUN apt update && apt install chromium -y && apt clean

WORKDIR /app/

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY script.py .

RUN DOCKER_BUILD=BUILD REQUEST_TIMEOUT_SECONDS=5 python -u /app/script.py

CMD [ "python", "-u", "/app/script.py" ]