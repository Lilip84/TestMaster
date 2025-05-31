from playwright.sync_api import sync_playwright
import requests
import logging
from .tester import UniversalTester

def execute_ui_test(test_config):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        try:
            for step in test_config['steps']:
                if step['action'] == 'navigate':
                    page.goto(step['url'])
                elif step['action'] == 'fill':
                    page.fill(step['selector'], step['value'])
                elif step['action'] == 'click':
                    page.click(step['selector'])
            
            return {"status": "passed", "screenshot": "data:image/png;base64,..."}
        except Exception as e:
            return {"status": "failed", "error": str(e)}
        finally:
            browser.close()

def execute_api_test(test_config):
    try:
        response = requests.request(
            method=test_config['method'],
            url=test_config['url'],
            json=test_config.get('body', None)
        )
        
        return {
            "status": "passed" if response.ok else "failed",
            "status_code": response.status_code,
            "response": response.json()
        }
    except Exception as e:
        return {"status": "failed", "error": str(e)}