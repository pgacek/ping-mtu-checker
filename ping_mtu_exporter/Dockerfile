FROM alpine:3.18.4

WORKDIR /app
COPY ./app/ /app/

RUN apk add --no-cache python3 py3-pip iputils && \
    pip install --no-cache-dir -r requirements.txt

ENV SERVER_PORT 5000

CMD ["python3", "main.py"]
