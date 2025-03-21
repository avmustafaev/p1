FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY avito_parser.py .
COPY bot.py .
COPY loadenv.py .

CMD ["python", "bot.py"]