import logging
import os
from typing import Optional

def setup_logger(name: str, log_file: Optional[str] = None, level: int = logging.INFO) -> logging.Logger:
    """
    Настраивает и возвращает логгер с заданным именем
    
    :param name: Имя логгера (обычно __name__)
    :param log_file: Путь к файлу для записи логов (опционально)
    :param level: Уровень логирования (по умолчанию INFO)
    :return: Сконфигурированный логгер
    """
    # 1. Создаем логгер
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # 2. Создаем форматтер
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # 3. Создаем консольный обработчик
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # 4. При необходимости добавляем файловый обработчик
    if log_file:
        # Создаем директорию для логов, если ее нет
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    # 5. Возвращаем сконфигурированный логгер
    return logger

# Пример использования в других файлах:
# from src.logger import setup_logger
# logger = setup_logger(__name__, log_file="logs/app.log")