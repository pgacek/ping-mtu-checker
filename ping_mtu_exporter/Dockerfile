FROM python:3.11-slim

WORKDIR /app
COPY ./app/ /app/
RUN apt-get update && apt-get install -y iputils-ping && \
    pip install --no-cache-dir -r requirements.txt

ENV SERVER_PORT 5000

CMD ["python", "main.py"]
