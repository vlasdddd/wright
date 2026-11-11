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
    
    # 1. Делаем первый скриншот (светлой темы)
    page.screenshot(path="light_theme.png")
    
    print("Браузер на экране. Пожалуйста, кликните на смену темы...")
    
    # 2. Ожидание вашего клика: код замирает, пока вы сами не нажмете на кнопку.
    # Как только тема переключится в коде на "dark" — тест мгновенно продолжится.
    page.wait_for_selector('html[data-theme="dark"]', timeout=15000)
    
    # 3. Делаем финальный скриншот после вашего нажатия
    page.screenshot(path="dark_theme.png")
    print("Тема изменена, скриншоты сохранены!")

# Этот блок принудительно открывает видимое окно браузера на экране при запуске через python
if __name__ == "__main__":
    pytest.main(["-v", "--headed", __file__])
