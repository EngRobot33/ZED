FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update -y && apt-get install npm  -y 

EXPOSE 8000

WORKDIR /code

COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY package.json . 
RUN npm install

COPY . . 

ENTRYPOINT ["/bin/sh","-c", "python3 manage.py migrate && python3 manage.py runserver 0.0.0.0:8000"]


