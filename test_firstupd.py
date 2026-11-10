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
