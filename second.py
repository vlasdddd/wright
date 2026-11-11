# ФИО: Зубов Владислав Витальевич
# Дата: 2026-11-11
# Время: 13:37
# Описание: Написал автоматические тесты для проверки работы с API Гитхаба без запуска браузера. Скрипт подключается к серверу, отправляет REST-запросы и проверяет, как создаются задачи (Issues) в репозитории.
# Код скопировал из Guides/ API testing
import os
import time
from typing import Generator
import pytest
from playwright.sync_api import Playwright, APIRequestContext

# Проверки наличия переменных окружения
GITHUB_API_TOKEN = os.getenv("GITHUB_API_TOKEN")
assert GITHUB_API_TOKEN, "GITHUB_API_TOKEN is not set"

GITHUB_USER = os.getenv("GITHUB_USER")
assert GITHUB_USER, "GITHUB_USER is not set"

# Имя вашего репозитория
GITHUB_REPO = "wright"

@pytest.fixture(scope="session")
def api_request_context(
    playwright: Playwright,
) -> Generator[APIRequestContext, None, None]:
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {GITHUB_API_TOKEN}",
    }
    request_context = playwright.request.new_context(
        base_url="https://api.github.com", extra_http_headers=headers
    )
    yield request_context
    request_context.dispose()

def test_should_create_bug_report(api_request_context: APIRequestContext) -> None:
    data = {
        "title": "[Bug] report 1",
        "body": "Bug description",
    }
    # Передаем словарь напрямую в data. Playwright сам сделает JSON.
    new_issue = api_request_context.post(f"/repos/{GITHUB_USER}/{GITHUB_REPO}/issues", data=data)
    
    if not new_issue.ok:
        print(f"\n[BUG REPORT] Ошибка от GitHub: {new_issue.status} - {new_issue.text()}")
    assert new_issue.ok

    # Ожидание для обновления базы данных GitHub
    time.sleep(1)

    issues = api_request_context.get(f"/repos/{GITHUB_USER}/{GITHUB_REPO}/issues")
    assert issues.ok
    issues_response = issues.json()
    
    issue = list(filter(lambda issue: issue["title"] == "[Bug] report 1", issues_response))
    assert issue
    assert issue[0]["body"] == "Bug description"

def test_should_create_feature_request(api_request_context: APIRequestContext) -> None:
    data = {
        "title": "[Feature] request 1",
        "body": "Feature description",
    }
    # Передаем словарь напрямую в data. Playwright сам сделает JSON.
    new_issue = api_request_context.post(f"/repos/{GITHUB_USER}/{GITHUB_REPO}/issues", data=data)
    
    if not new_issue.ok:
        print(f"\n[FEATURE REQUEST] Ошибка от GitHub: {new_issue.status} - {new_issue.text()}")
    assert new_issue.ok

    # Ожидание для обновления базы данных GitHub
    time.sleep(1)

    issues = api_request_context.get(f"/repos/{GITHUB_USER}/{GITHUB_REPO}/issues")
    assert issues.ok
    issues_response = issues.json()
    
    issue = list(filter(lambda issue: issue["title"] == "[Feature] request 1", issues_response))
    assert issue
    assert issue[0]["body"] == "Feature description"

if __name__ == "__main__":
    pytest.main(["-v", __file__])
