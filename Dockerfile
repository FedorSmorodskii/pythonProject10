FROM python:3.9-slim

RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY main.py .

RUN pip install --no-cache-dir gitpython requests

# Настраиваем Git с сохранением учетных данных
RUN git config --global credential.helper store && \
    git config --global user.name "Code Generator" && \
    git config --global user.email "generator@example.com"

# Создаем файл с учетными данными при старте
CMD echo "https://${GITHUB_TOKEN}:x-oauth-basic@github.com" > ~/.git-credentials && \
    python main.py