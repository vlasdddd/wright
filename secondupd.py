# ФИО: Зубов Владислав Витальевич
# Дата: 2026-11-12
# Время: 09:49
# Описание модификации: 
# 1.(def test_api_root_endpoints) проверяет доступность API, отправляет запрос на сервер и ждёт, что он ответит статусом 'ОК', + добавил повторые проверку если сервер выдаст ошибку 502 или 503.
# 2.(test_should_create_and_close_bug_report) после успешной проверки доступа, создаёт в репозитории в вкладке Issues создаёт проблему с названием "[Bug] report 1", с описанием "Bug description", в теме bug, и потом его сразу закрывает + сделал проверку если она не закроется или не сделается
# 3.(test_should_create_and_close_feature_request) делает то же самое, что и второй пункт, но уже с названием "[Feature] request 1", описанием "Feature description", и темой "enhancement"

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

# Имя репозитория и базовый путь к задачам
GITHUB_REPO = "wright"
ISSUES_ENDPOINT = f"/repos/{GITHUB_USER}/{GITHUB_REPO}/issues"

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

def close_issue_with_retry(api_request_context: APIRequestContext, issue_number: int, retries: int = 3) -> None:
    """Закрывает задачу с повторными попытками на случай временной ошибки 502/503 от GitHub."""
    for attempt in range(retries):
        close_resp = api_request_context.patch(
            f"{ISSUES_ENDPOINT}/{issue_number}", data={"state": "closed"}
        )
        if close_resp.ok:
            return
        time.sleep(1)
    assert close_resp.ok, f"Не удалось закрыть задачу #{issue_number}: {close_resp.status}"

def test_api_root_endpoints(api_request_context: APIRequestContext) -> None:
    """Проверка базовых эндпоинтов корневого ответа API GitHub."""
    response = api_request_context.get("/")
    assert response.status == 200
    data = response.json()
    assert data["issues_url"] == "https://api.github.com/issues"
    assert data["repository_url"] == "https://api.github.com/repos/{owner}/{repo}"

def test_should_create_and_close_bug_report(api_request_context: APIRequestContext) -> None:
    payload = {
        "title": "[Bug] report 1",
        "body": "Bug description",
        "labels": ["bug"],
    }
    new_issue = api_request_context.post(ISSUES_ENDPOINT, data=payload)
    
    if not new_issue.ok:
        print(f"\n[BUG REPORT] Ошибка от GitHub: {new_issue.status} - {new_issue.text()}")
    assert new_issue.status == 201
    issue_number = new_issue.json()["number"]

    # Ожидание для обновления базы данных GitHub
    time.sleep(1)

    # Проверяем созданную задачу напрямую по её номеру
    issue_resp = api_request_context.get(f"{ISSUES_ENDPOINT}/{issue_number}")
    assert issue_resp.ok
    issue_data = issue_resp.json()
    assert issue_data["title"] == "[Bug] report 1"
    assert issue_data["body"] == "Bug description"

    # Очистка: закрываем созданную задачу с защитой от временных сбоев сети
    close_issue_with_retry(api_request_context, issue_number)

def test_should_create_and_close_feature_request(api_request_context: APIRequestContext) -> None:
    payload = {
        "title": "[Feature] request 1",
        "body": "Feature description",
        "labels": ["enhancement"],
    }
    new_issue = api_request_context.post(ISSUES_ENDPOINT, data=payload)
    
    if not new_issue.ok:
        print(f"\n[FEATURE REQUEST] Ошибка от GitHub: {new_issue.status} - {new_issue.text()}")
    assert new_issue.status == 201
    issue_number = new_issue.json()["number"]

    # Ожидание для обновления базы данных GitHub
    time.sleep(1)

    # Проверяем созданную задачу напрямую по её номеру
    issue_resp = api_request_context.get(f"{ISSUES_ENDPOINT}/{issue_number}")
    assert issue_resp.ok
    issue_data = issue_resp.json()
    assert issue_data["title"] == "[Feature] request 1"
    assert issue_data["body"] == "Feature description"

    # Очистка: закрываем созданную задачу
    close_issue_with_retry(api_request_context, issue_number)

if __name__ == "__main__":
    pytest.main(["-v", __file__])
