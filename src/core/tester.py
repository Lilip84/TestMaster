from playwright.sync_api import sync_playwright
import requests
from sqlalchemy import create_engine, text
import logging

class UniversalTester:
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger('TestMaster')
        
        # Инициализация подключений
        if config.DB_URL:
            self.db_engine = create_engine(config.DB_URL)
        if config.API_BASE_URL:
            self.api_base_url = config.API_BASE_URL
        if config.WEB_BASE_URL:
            self.web_base_url = config.WEB_BASE_URL
    
    def test_ui(self, test_config):
        # Использует execute_ui_test из executor.py
        pass
    
    def test_api(self, endpoint, method='GET', payload=None):
        url = f"{self.api_base_url}{endpoint}"
        return requests.request(method, url, json=payload)
    
    def test_db(self, query):
        with self.db_engine.connect() as conn:
            result = conn.execute(text(query))
            return result.fetchall()
    
    def run_test(self, test_type, test_data):
        if test_type == 'ui':
            return self.test_ui(test_data)
        elif test_type == 'api':
            return self.test_api(test_data)
        elif test_type == 'db':
            return self.test_db(test_data)