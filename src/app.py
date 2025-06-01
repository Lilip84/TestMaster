# src/app.py

import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from src.core.auth import User
from src.celery_worker import run_ui_test, run_api_test, run_db_check
from src.config import Config
from celery.result import AsyncResult
from src.logger import setup_logger
from typing import Optional, Dict, Any
from dotenv import load_dotenv
import requests
from sqlalchemy import create_engine
from src.core.config_db import ConfigDB

# Загрузка переменных окружения
load_dotenv()

# Создание приложения Flask
app = Flask(__name__)

# Глобальная переменная для временного хранения настроек
global_config = {}

# Конфигурация приложения
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key_here')
    PORT = int(os.getenv('PORT', 5000))
    DB_URL = os.getenv('DB_URL', 'sqlite:///test.db')
    API_BASE_URL = os.getenv('API_BASE_URL', 'https://api.example.com')
    WEB_BASE_URL = os.getenv('WEB_BASE_URL', 'https://example.com')
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin')
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'test123')
    TEST_CASES_DIR = os.getenv('TEST_CASES_DIR', 'test_cases')
    TEST_CHAINS_DIR = os.getenv('TEST_CHAINS_DIR', 'test_chains')

app.config.from_object(Config)

# Настройка логирования
logger = setup_logger('TestMasterApp')

# Инициализация LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id: str) -> Optional[User]:
    """Загрузка пользователя для Flask-Login"""
    return User.get(user_id)

# Маршрут для страницы настроек
@app.route('/settings', methods=['GET', 'POST'])
@login_required
def connection_settings():
    """
    Маршрут для страницы настроек подключений.
    Доступен только авторизованным пользователям.
    """
    if request.method == 'POST':
        # Получаем данные из формы
        web_base_url = request.form['web_base_url']
        api_base_url = request.form['api_base_url']
        db_url = request.form['db_url']
        
        # Сохраняем полученные данные (пример простой реализации через глобальную переменную)
        global_config.update({
            'WEB_BASE_URL': web_base_url,
            'API_BASE_URL': api_base_url,
            'DB_URL': db_url
        })
        
        # Показываем уведомление о сохранении
        flash('Настройки сохранены!', category='success')
        return redirect(url_for('connection_settings'))
    
    # Передаем текущие настройки в шаблон
    return render_template('connection_settings.html', config=global_config)

# Главные роуты
@app.route('/')
@login_required
def control_panel() -> str:
    """Главная панель управления"""
    return render_template('control_panel.html')

@app.route('/editor')
@login_required
def editor() -> str:
    """Редактор тест-кейсов"""
    return render_template('editor.html')

@app.route('/test-chain-editor')
@login_required
def test_chain_editor() -> str:
    """Визуальный конструктор цепочек тестов"""
    return render_template('test_chain_editor.html')

@app.route('/load-testing')
@login_required
def load_testing() -> str:
    """Панель нагрузочного тестирования"""
    return render_template('load_testing.html')

# Новые роуты для тестирования соединений
@app.route('/api/test-connection/web', methods=['GET'])
@login_required
def test_web_connection():
    try:
        url = ConfigDB.get_connection('web_base_url')
        if not url:
            return jsonify({
                "success": False,
                "message": "URL веб-приложения не настроен",
                "type": "web"
            })
        
        response = requests.get(url, timeout=5)
        return jsonify({
            "success": True,
            "message": f"Успешное подключение! Статус: {response.status_code}",
            "type": "web",
            "status_code": response.status_code
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Ошибка подключения: {str(e)}",
            "type": "web",
            "details": f"URL: {url}"
        })

@app.route('/api/test-connection/api', methods=['GET'])
@login_required
def test_api_connection():
    try:
        url = ConfigDB.get_connection('api_base_url')
        if not url:
            return jsonify({
                "success": False,
                "message": "URL API не настроен",
                "type": "api"
            })
        
        response = requests.get(url, timeout=5)
        return jsonify({
            "success": True,
            "message": f"API доступен! Статус: {response.status_code}",
            "type": "api",
            "status_code": response.status_code
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Ошибка подключения к API: {str(e)}",
            "type": "api",
            "details": f"URL: {url}"
        })

@app.route('/api/test-connection/db', methods=['GET'])
@login_required
def test_db_connection():
    try:
        db_url = ConfigDB.get_connection('db_url')
        if not db_url:
            return jsonify({
                "success": False,
                "message": "URL базы данных не настроен",
                "type": "db"
            })
        
        engine = create_engine(db_url)
        with engine.connect() as conn:
            result = conn.execute("SELECT 1")
            if result.scalar() == 1:
                return jsonify({
                    "success": True,
                    "message": "Успешное подключение к базе данных",
                    "type": "db"
                })
        
        return jsonify({
            "success": False,
            "message": "Неожиданный результат теста БД",
            "type": "db"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Ошибка подключения к БД: {str(e)}",
            "type": "db",
            "details": f"Connection string: {db_url}"
        })

# API роуты
@app.route('/api/run-test', methods=['POST'])
@login_required
def run_test() -> jsonify:
    """
    Запускает выполнение теста асинхронно
    Требует JSON: { "test_id": "123", "type": "ui" }
    """
    try:
        data: Dict[str, Any] = request.json
        if not data:
            logger.error("Run test request without JSON data")
            return jsonify({"error": "Request body must be JSON"}), 400
        
        test_id: Optional[str] = data.get('test_id')
        test_type: Optional[str] = data.get('type', 'ui')
        
        # Валидация входных данных
        if not test_id:
            logger.error("Missing 'test_id' in run test request")
            return jsonify({"error": "Missing 'test_id' parameter"}), 400
        
        if test_type not in ['ui', 'api', 'db']:
            logger.error(f"Invalid test type: {test_type}")
            return jsonify({"error": "Invalid test type. Use 'ui', 'api' or 'db'"}), 400
        
        # Здесь должна быть логика получения теста по ID
        # Пока используем заглушку
        test_data = {
            "id": test_id,
            "type": test_type,
            "name": f"Test {test_id}",
            "config": {
                "steps": [
                    {"action": "navigate", "url": "https://example.com/login"},
                    {"action": "fill", "selector": "#username", "value": "admin"},
                    {"action": "fill", "selector": "#password", "value": "test123"},
                    {"action": "click", "selector": "#login-button"}
                ]
            }
        }
        
        # Выбор задачи Celery по типу теста
        task_mapping = {
            'ui': run_ui_test,
            'api': run_api_test,
            'db': run_db_check
        }
        
        task = task_mapping[test_type].delay(test_data)
        logger.info(f"Started test {test_id} (type: {test_type}), task ID: {task.id}")
        
        return jsonify({
            "status": "started",
            "task_id": task.id,
            "test_id": test_id,
            "test_type": test_type
        })
    
    except Exception as e:
        logger.exception(f"Error running test: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

# Роуты аутентификации сохраняются такими же...

# Запуск приложения
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=Config.PORT, debug=os.getenv('FLASK_DEBUG', 'False') == 'True')