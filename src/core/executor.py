from playwright.sync_api import sync_playwright, Page
import requests
from sqlalchemy import create_engine, text
import base64
import logging
from typing import Dict, Any, List, Union, Optional

# Настройка логгера
logger = logging.getLogger('TestExecutor')

def execute_ui_test(test_config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Выполняет UI тест с использованием Playwright
    
    :param test_config: Конфигурация теста
    :return: Результаты выполнения
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        try:
            # Выполнение всех шагов теста
            for step in test_config.get('steps', []):
                execute_step(page, step)
            
            # Создание скриншота
            screenshot = page.screenshot(type="png")
            screenshot_b64 = base64.b64encode(screenshot).decode('utf-8')
            
            return {
                "status": "passed",
                "screenshot": f"data:image/png;base64,{screenshot_b64}",
                "steps_count": len(test_config.get('steps', []))
            }
        except Exception as e:
            logger.error(f"UI test failed: {str(e)}")
            return {
                "status": "failed",
                "error": str(e),
                "steps_count": len(test_config.get('steps', []))
            }
        finally:
            browser.close()

def execute_step(page: Page, step: Dict[str, Any]) -> None:
    """
    Выполняет один шаг UI теста
    
    :param page: Экземпляр страницы Playwright
    :param step: Конфигурация шага
    """
    action = step.get('action')
    
    if not action:
        raise ValueError("Step is missing 'action' field")
    
    if action == 'navigate':
        page.goto(step['url'])
    elif action == 'fill':
        page.fill(step['selector'], step['value'])
    elif action == 'click':
        page.click(step['selector'])
    elif action == 'wait':
        page.wait_for_timeout(step.get('timeout', 1000))
    else:
        raise ValueError(f"Unknown action: {action}")

def execute_api_test(test_config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Выполняет API тест
    
    :param test_config: Конфигурация теста
    :return: Результаты выполнения
    """
    try:
        method = test_config.get('method', 'GET')
        url = test_config['url']
        payload = test_config.get('payload')
        
        response = requests.request(
            method=method,
            url=url,
            json=payload,
            timeout=10
        )
        
        return {
            "status": "success" if response.ok else "failed",
            "status_code": response.status_code,
            "response": response.json() if response.content else None
        }
    except Exception as e:
        logger.error(f"API test failed: {str(e)}")
        return {
            "status": "failed",
            "error": str(e)
        }

def execute_db_check(test_config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Выполняет проверку в базе данных
    
    :param test_config: Конфигурация теста
    :return: Результаты выполнения
    """
    try:
        db_url = test_config['db_url']
        query = test_config['query']
        
        engine = create_engine(db_url)
        with engine.connect() as conn:
            result = conn.execute(text(query))
            
            # Конвертация результатов в словари
            columns = result.keys()
            rows = [dict(zip(columns, row)) for row in result.fetchall()]
            
            return {
                "status": "success",
                "row_count": len(rows),
                "data": rows
            }
    except Exception as e:
        logger.error(f"DB check failed: {str(e)}")
        return {
            "status": "failed",
            "error": str(e)
        }