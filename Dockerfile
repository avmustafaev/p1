FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && \
    apt-get install -y --no-install-recommends chromium chromium-driver && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY avito_parser.py .

CMD ["python", "avito_parser.py"]