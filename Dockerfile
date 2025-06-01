FROM python:3.10-slim

WORKDIR /app

# Установка Python зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Установка Playwright и браузеров
RUN playwright install && playwright install-deps

# Копирование всего проекта
COPY . .

# Установка переменной окружения для Python
ENV PYTHONPATH=/app

CMD ["python", "src/app.py"]