@echo off
echo Установка TestMaster для Windows...

:: Проверка Python
python --version
if %errorlevel% neq 0 (
    echo Установка Python...
    winget install Python.Python.3.10
    refreshenv
)

:: Установка Docker
docker --version
if %errorlevel% neq 0 (
    echo Установка Docker Desktop...
    winget install Docker.DockerDesktop
    echo Запустите Docker Desktop после установки и нажмите Enter
    pause
)

:: Создание виртуального окружения
python -m venv testmaster-env
call testmaster-env\Scripts\activate

:: Установка зависимостей
pip install flask flask-login flask-admin playwright locust faker gitpython

:: Инициализация Playwright
playwright install

echo ==========================================
echo ✅ Зависимости успешно установлены!
echo 👉 Скопируйте Part2 и Part3 в эту папку
echo 👉 Запустите: scripts\run.bat
echo ==========================================
pause