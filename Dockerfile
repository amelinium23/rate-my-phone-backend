FROM python:3.9

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt
CMD gunicorn main.app:rate_my_phone_app
