FROM python:3.10-slim
run apt-get update -y && apt-get install npm  -y 

expose 8000

WORKDIR /code

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY package.json . 
run npm install

copy . . 

entrypoint ["/bin/sh","-c", "python3 manage.py migrate && python3 manage.py runserver 0.0.0.0:8000"]


