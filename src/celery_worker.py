from celery import Celery
from src.app import Config

celery = Celery(
    'tasks',
    broker=Config.CELERY_BROKER_URL,
    backend=Config.CELERY_BROKER_URL
)

@celery.task
def run_ui_test(test_data):
    # Здесь будет логика выполнения UI-теста
    return {"status": "completed", "result": "success"}