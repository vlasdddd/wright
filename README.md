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
результат дня загружен на GitHub под коммитом "Первый день"
```
