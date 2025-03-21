FROM python:3.11-slim

WORKDIR /app

# Устанавливаем wget и другие необходимые утилиты
RUN apt-get update && \
    apt-get install -y --no-install-recommends wget && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Устанавливаем Firefox и Geckodriver
RUN apt-get update && \
    apt-get install -y --no-install-recommends firefox-esr && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Скачиваем и устанавливаем Geckodriver
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.34.0/geckodriver-v0.34.0-linux64.tar.gz -O /tmp/geckodriver.tar.gz && \
    tar -xzf /tmp/geckodriver.tar.gz -C /usr/local/bin/ && \
    chmod +x /usr/local/bin/geckodriver && \
    rm /tmp/geckodriver.tar.gz

# Копируем зависимости и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем основной скрипт
COPY avito_parser.py .

CMD ["python", "avito_parser.py"]