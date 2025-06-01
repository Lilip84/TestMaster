import os

class Config:
    # Веб-сервер
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key_here')
    PORT = int(os.getenv('PORT', 5000))
    
    # База данных (SQLite/PostgreSQL)
    DB_URL = os.getenv('DATABASE_URL', 'sqlite:///test.db')
    
    # API и UI тестирование
    API_BASE_URL = os.getenv('API_BASE_URL', 'https://api.example.com')
    WEB_BASE_URL = os.getenv('WEB_BASE_URL', 'https://example.com')
    
    # Celery (Redis)
    CELERY_BROKER_URL = os.getenv('REDIS_URL', 'redis://redis:6379/0')
    
    # Аутентификация
    ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin')
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'test123')
    
    # Пути
    TEST_CASES_DIR = os.getenv('TEST_CASES_DIR', 'test_cases')
    TEST_CHAINS_DIR = os.getenv('TEST_CHAINS_DIR', 'test_chains')
    
    @staticmethod
    def init_app(app):
        # Устанавливаем секретный ключ
        app.secret_key = os.environ.get('SECRET_KEY', app.config['SECRET_KEY'])
        
        # Другие действия инициализации
        print("Application configuration initialized.")