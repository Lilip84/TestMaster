@echo off
REM Запуск Docker контейнера с Redis
docker start testmaster-redis 2>nul || docker run -d -p 6379:6379 --name testmaster-redis redis

REM Активация виртуального окружения
call .\testmaster-env\Scripts\activate

REM Запуск Flask и Celery в фоновом режиме
start /B python src\app.py
start /B celery -A src.celery_worker.celery worker --loglevel=info -P eventlet

REM Открытие браузера
timeout /t 3
start http://localhost:5000

echo TestMaster запущен! Для остановки закройте это окно.
pause