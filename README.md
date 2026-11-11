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
