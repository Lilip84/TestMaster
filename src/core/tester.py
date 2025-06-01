import logging
from typing import Dict, Any, Union, List, Optional
from .executor import execute_ui_test, execute_api_test, execute_db_check
from src.core.config_db import ConfigDB

class UniversalTester:
    """Универсальный класс для выполнения различных типов тестов"""
    
    def __init__(self):
        """
        Инициализация тестера
        Загружаем настройки при запуске экземпляра
        """
        self.config = ConfigDB.load_connections()
        self.logger = logging.getLogger('UniversalTester')
    
    @property
    def web_base_url(self):
        return self.config.get('web_base_url', '')
    
    @property
    def api_base_url(self):
        return self.config.get('api_base_url', '')
    
    @property
    def db_url(self):
        return self.config.get('db_url', '')
    
    def test_ui(self, test_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Выполняет UI-тест
        """
        test_config['base_url'] = self.web_base_url
        try:
            return execute_ui_test(test_config)
        except Exception as e:
            self.logger.error(f"UI test execution failed: {str(e)}")
            return {
                "status": "failed",
                "error": str(e)
            }
    
    def test_api(self, test_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Выполняет API-тест
        """
        test_config['base_url'] = self.api_base_url
        try:
            return execute_api_test(test_config)
        except Exception as e:
            self.logger.error(f"API test execution failed: {str(e)}")
            return {
                "status": "failed",
                "error": str(e)
            }
    
    def test_db(self, test_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Выполняет проверку базы данных
        """
        test_config['db_url'] = self.db_url
        try:
            return execute_db_check(test_config)
        except Exception as e:
            self.logger.error(f"DB check execution failed: {str(e)}")
            return {
                "status": "failed",
                "error": str(e)
            }
    
    def run_test(self, test_type: str, test_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Запускает тест указанного типа
        """
        handlers = {
            'ui': self.test_ui,
            'api': self.test_api,
            'db': self.test_db
        }
        
        if test_type not in handlers:
            return {
                "status": "error",
                "error": f"Unsupported test type: {test_type}"
            }
        
        return handlers[test_type](test_data)