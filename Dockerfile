FROM python:3.10-alpine
WORKDIR /app
COPY . /app

RUN apt update -y && apt install awscli -y
RUN apt-get update -y && pip install -r requirements.txt

CMD ["python3", "app.py"]