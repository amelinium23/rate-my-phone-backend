FROM python:latest

ADD . /app
ADD google-credentials.json /app
WORKDIR /app

RUN pip3 install -r requirements.txt
CMD python3 gunicorn wsgi.py
