FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update -y && apt-get install npm  -y 

EXPOSE 9000

WORKDIR /code

COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY package.json . 
RUN npm install

COPY . . 

RUN chmod +x run.sh

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl --fail --location http://localhost:9000/auth/signup/ || exit 1

STOPSIGNAL SIGTERM
ENTRYPOINT [ "/bin/bash", "-l", "-c" ]
CMD ["/bin/bash"]


