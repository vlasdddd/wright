# Первый день

```python
# ФИО: Зубов Владислав Витальевич
# Дата: 2026-11-09
# Время: 10:44
# Описание: Тест запускает браузер Chromium в фоновом режиме, открывает стартовую страницу и проверяет правильность её работы
# Я скопировал пример из раздела "Writing tests" и запустил его локально.

import pytest
from playwright.sync_api import Page, expect

# Фикстура выполняется автоматически для каждого теста
@pytest.fixture(scope="function", autouse=True)
def before_each_after_each(page: Page):
    # Код перед запуском самого теста
    print("before the test runs")
    page.goto("https://playwright.dev/")
    
    yield
    
    # Код, который сработает сразу после окончания теста
    print("after the test runs")

# Тест проверяет, что браузер успешно перешел по нужному адресу
def test_main_navigation(page: Page):
    expect(page).to_have_url("https://playwright.dev/")
```

# Результат запуска

```text
Код выполнен без ошибок. Тест успешно прошёл проверку (1 passed).
```

# Ежедневный коммит на GitHub

```text
Результат дня загружен на GitHub под коммитом "Первый день"
```
# Второй день 
```python
# ФИО: Зубов Владислав Витальевич
# Дата: 2026-11-11
# Описание изменений: добавил сохранение двух скриншотов и автоматическое закрытие окна сразу после ручного клика по смене темы

import pytest
from playwright.sync_api import Page, expect

@pytest.fixture(scope="function", autouse=True)
def before_each_after_each(page: Page):
    print("before the test runs")
    page.goto("https://playwright.dev/")
    yield
    print("after the test runs")

def test_main_navigation(page: Page):
    # Убеждаемся, что страница загрузилась
    page.wait_for_load_state("load")
    
    # Делаем первый скриншот (светлой темы)
    page.screenshot(path="light_theme.png")
    
    print("Браузер на экране. Пожалуйста, кликните на смену темы...")
    
    # Ожидание вашего клика: код замирает, пока вы сами не нажмете на кнопку.
    # Как только тема переключится в коде на "dark" — тест мгновенно продолжится.
    page.wait_for_selector('html[data-theme="dark"]', timeout=15000)
    
    # Делаем финальный скриншот после вашего нажатия
    page.screenshot(path="dark_theme.png")
    print("Тема изменена, скриншоты сохранены!")

# Этот блок принудительно открывает видимое окно браузера на экране при запуске через python
if __name__ == "__main__":
    pytest.main(["-v", "--headed", __file__])
```

# Результат запуска

```text
Код успешно запустился, сначала сделал скриншот белой темы, при клике на кнопку смены на тёмную, сделался скриншот тёмной темы.
```
# Ежедневный коммит на GitHub

```text
Результат дня загружен на GitHub под коммитом "День второй, модификация первого первого кода"
```

# Третий день

```python
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
```
# Результат запуска

```text
В результате успешного запуска кода тесты полностью прошли проверку (2 passed), автоматически создав в репозитории две реальные задачи: баг-репорт и запрос новой функции.
```

# Ежедневный коммит на GitHub

```text
Результат дня загружен на GitHub под коммитом "День третий(Добавил второй код)"
```
# Четвёртый день

```python
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
```

# Результат запуска

```text
collected 3 items                                                                                                                                                                                                       

wright/secondupd.py::test_api_root_endpoints PASSED                                                                                                                                                               [ 33%]
wright/secondupd.py::test_should_create_and_close_bug_report PASSED                                                                                                                                               [ 66%]
wright/secondupd.py::test_should_create_and_close_feature_request PASSED                                                                                                                                          [100%]

=================================================================================================== 3 passed in 6.03s ===================================================================================================

Сначала код проверил доступность API, а после этого 
На гитхабе в вкладке Issue создались 2 проблемы, каждый с своим названием, с своей темой, с своим описанием и через некоторое время автоматически закрылись
```

# Ежедневный коммит на GitHub

```text
Результат дня загружен на GitHub под коммитом "День четвертый(модификация второго кода)"
```
