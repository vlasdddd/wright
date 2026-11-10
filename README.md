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
# Второй день 
```python
# ФИО: Зубов Владислав Витальевич
# Дата: 2026-11-10
# Описание изменений:Добавил автоматическое сохранение двух скриншотов, если нажимаем на смену темы, добавил проверку смены кода

import pytest
from playwright.sync_api import Page, expect

def test_visual_theme_switch(page: Page):
    # Переходим на сайт
    page.goto("https://playwright.dev")
    page.wait_for_load_state("load")
    
    # Делаем скриншот светлой темы
    page.screenshot(path="light_theme.png")
    
    # Нажимаем на кнопку смены темы
    page.get_by_role("button", name="Switch between dark and light mode").click()
    page.wait_for_timeout(1000)
    
    # Проверяем, что тема действительно переключилась в коде
    expect(page.locator("html")).to_have_attribute("data-theme", "dark")
    
    # Делаем скриншот темной темы
    page.screenshot(path="dark_theme.png")

# Этот блок заставит файл самостоятельно скормить себя фреймворку pytest
if __name__ == "__main__":
    pytest.main(["-v", "--headed", __file__])
```

# Результат запуска

```text
Код успешно запустился, сначала сделал скриншот белой темы, при клике на кнопку смены на тёмную, сразу после этого сделался скриншот тёмной темы.
```
# Ежедневный коммит на GitHub

```text
результат дня загружен на GitHub под коммитом "День второй, модификация первого первого кода"
```
