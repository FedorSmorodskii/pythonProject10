# Используем официальный образ Python
FROM python:3.9-slim

# Устанавливаем зависимости
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Создаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта
COPY main.py .

# Устанавливаем зависимости Python
RUN pip install --no-cache-dir \
    gitpython \
    requests

# Настраиваем Git (базовые настройки)
RUN git config --global init.defaultBranch main

# Запускаем скрипт
CMD ["python", "main.py"]