import os

class Config:
    # Веб-сервер
    SECRET_KEY = "your_secret_key_here"
    PORT = 5000
    
    # База данных (SQLite/PostgreSQL)
    DB_URL = "sqlite:///test.db"
    
    # API и UI тестирование
    API_BASE_URL = "https://api.example.com"
    WEB_BASE_URL = "https://example.com"
    
    # Celery (Redis)
    CELERY_BROKER_URL = "redis://localhost:6379/0"
    
    # Аутентификация
    ADMIN_USERNAME = "admin"
    ADMIN_PASSWORD = "test123"
    
    # Пути
    TEST_CASES_DIR = "test_cases"
    TEST_CHAINS_DIR = "test_chains"
    
    @staticmethod
    def init_app(app):
        pass