# Dockerfile
FROM python:3.10-slim

RUN apt-get update && \
    apt-get install -y git git-lfs && \
    git lfs install

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 4500

CMD ["python", "app/app.py"]
