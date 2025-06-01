# TestMaster - Фреймворк для сквозного тестирования

**TestMaster** - это универсальный фреймворк для автоматизации тестирования веб-приложений, включая UI, API, базы данных и нагрузочное тестирование.

## Особенности
- Тестирование UI (Playwright)
- Тестирование API (Requests)
- Проверки базы данных (SQLAlchemy)
- Нагрузочное тестирование (Locust)
- Генерация тестовых данных (Faker)
- Веб-интерфейс для управления тестами

## Установка
1. Скопируйте все 3 части архива в одну папку
2. Запустите установочный скрипт:
   - Linux/macOS: `./scripts/install.sh`
   - Windows: `scripts\install.bat`
3. После установки зависимостей запустите систему:
   - Linux/macOS: `./scripts/run.sh`
   - Windows: `scripts\run.bat`

Откройте в браузере: http://localhost:5000  
**Логин:** admin  
**Пароль:** test123

## Технологический стек
- Python 3.10+
- Flask (веб-сервер)
- Celery (асинхронные задачи)
- Redis (брокер сообщений)
- Playwright (браузерная автоматизация)
- SQLAlchemy (работа с БД)
- Locust (нагрузочное тестирование)

## Полная инструкция для запуска:
# 1. Перейдите в папку проекта
cd C:\Users\lilip\OneDrive\Рабочий стол\TestMaster

# 2. Активируйте виртуальное окружение
.\testmaster-env\Scripts\activate

# 3. Добавьте проект в PYTHONPATH
$env:PYTHONPATH = "$env:PYTHONPATH;$pwd"

# 4. Запустите Redis
docker start testmaster-redis || docker run -d -p 6379:6379 --name testmaster-redis redis

# 5. Запустите Flask приложение
python src\app.py

В отдельном окне PowerShell:
# 1. Перейдите в папку проекта
cd C:\Users\lilip\OneDrive\Рабочий стол\TestMaster

# 2. Активируйте виртуальное окружение
.\testmaster-env\Scripts\activate

# 3. Добавьте проект в PYTHONPATH
$env:PYTHONPATH = "$env:PYTHONPATH;$pwd"

# 4. Запустите Celery
celery -A src.celery_worker.celery worker --loglevel=info -P eventlet