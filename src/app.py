from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from core.auth import User, load_user
from core.executor import execute_test
from core.tester import UniversalTester
from core.git_integration import GitManager
import os
import logging
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your_secret_key')

# Конфигурация
class Config:
    DB_URL = os.getenv('DB_URL', 'sqlite:///test.db')
    API_BASE_URL = os.getenv('API_BASE_URL', 'https://api.example.com')
    WEB_BASE_URL = os.getenv('WEB_BASE_URL', 'https://example.com')
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    TEST_CASES_DIR = 'test_cases'
    TEST_CHAINS_DIR = 'test_chains'
    ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin')
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'test123')

# Инициализация LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

# Главная панель
@app.route('/')
@login_required
def control_panel():
    return render_template('control_panel.html')

# Редактор тестов
@app.route('/editor')
@login_required
def editor():
    return render_template('editor.html')

# API для запуска тестов
@app.route('/api/run-test', methods=['POST'])
@login_required
def run_test():
    test_data = request.json
    test_id = test_data.get('test_id')
    
    # Здесь будет логика поиска и выполнения теста
    return jsonify({"status": "started", "task_id": "12345"})

# Логин
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == Config.ADMIN_USERNAME and password == Config.ADMIN_PASSWORD:
            user = User(1)
            login_user(user)
            return redirect(url_for('control_panel'))
    
    return render_template('login.html')

# Логаут
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)