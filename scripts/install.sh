#!/bin/bash

# Проверка и установка Python
if ! command -v python3 &> /dev/null; then
    echo "Установка Python..."
    sudo apt update
    sudo apt install -y python3 python3-pip
fi

# Проверка и установка Docker
if ! command -v docker &> /dev/null; then
    echo "Установка Docker..."
    sudo apt install -y docker.io
    sudo systemctl start docker
    sudo systemctl enable docker
fi

# Создание виртуального окружения
python3 -m venv testmaster-env
source testmaster-env/bin/activate

# Установка зависимостей
pip install flask flask-login flask-admin playwright locust faker gitpython

# Инициализация Playwright
playwright install

echo "=========================================="
echo "✅ Зависимости успешно установлены!"
echo "👉 Скопируйте Part2 и Part3 в эту папку"
echo "👉 Запустите: ./scripts/run.sh"
echo "=========================================="