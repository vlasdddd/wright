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
