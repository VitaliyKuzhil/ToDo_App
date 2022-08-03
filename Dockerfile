FROM python:3.9.5-slim-buster
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /django
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt