FROM python:3.10-slim
run apt-get update -y && apt-get install npm  -y 

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY package.json . 
run npm install

copy . . 

EXPOSE 8000



