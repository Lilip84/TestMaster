from celery import Celery
from .core.executor import execute_ui_test, execute_api_test, execute_db_check
from src.config import Config
from src.logger import setup_logger
from typing import Dict, Any

# Настройка логгера
logger = setup_logger('CeleryWorker')

# Инициализация Celery
celery = Celery(
    'tasks',
    broker=Config.CELERY_BROKER_URL,
    backend=Config.CELERY_BROKER_URL
)

@celery.task
def run_ui_test(test_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Задача Celery для выполнения UI теста
    
    :param test_data: Данные для теста
    :return: Результаты выполнения
    """
    try:
        logger.info(f"Starting UI test: {test_data.get('name', 'Unnamed')}")
        result = execute_ui_test(test_data)
        logger.info(f"UI test completed: {result['status']}")
        return result
    except Exception as e:
        logger.exception(f"UI test failed: {str(e)}")
        return {"status": "failed", "error": str(e)}

@celery.task
def run_api_test(test_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Задача Celery для выполнения API теста
    
    :param test_data: Данные для теста
    :return: Результаты выполнения
    """
    try:
        logger.info(f"Starting API test: {test_data.get('endpoint', 'Unknown')}")
        result = execute_api_test(test_data)
        logger.info(f"API test completed: {result['status']}")
        return result
    except Exception as e:
        logger.exception(f"API test failed: {str(e)}")
        return {"status": "failed", "error": str(e)}

@celery.task
def run_db_check(test_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Задача Celery для выполнения проверки БД
    
    :param test_data: Данные для теста
    :return: Результаты выполнения
    """
    try:
        logger.info(f"Starting DB check: {test_data.get('query', 'Unknown')}")
        result = execute_db_check(test_data)
        logger.info(f"DB check completed: {result['status']}")
        return result
    except Exception as e:
        logger.exception(f"DB check failed: {str(e)}")
        return {"status": "failed", "error": str(e)}