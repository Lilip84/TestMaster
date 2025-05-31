#!/bin/bash

# Активируем виртуальное окружение
source testmaster-env/bin/activate

# Запускаем Redis в Docker
docker run -d -p 6379:6379 --name testmaster-redis redis

# Запускаем Flask-приложение
cd src
python app.py &

# Запускаем Celery
celery -A app.celery worker --loglevel=info &

echo "=========================================="
echo "✅ TestMaster запущен!"
echo "👉 Откройте: http://localhost:5000"
echo "👉 Логин: admin, Пароль: test123"
echo "=========================================="