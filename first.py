# ФИО: Зубов Владислав Витальевич
# Дата: 2026-11-09
# Время: 10:44
# Описание: Тест test_main_navigation запускает браузер Chromium в фоновом режиме, открывает стартовую страницу и проверяет правильность её работы
# Я скопировал пример из раздела "Writing tests" и запустил его локально.

import pytest
from playwright.sync_api import Page, expect

@pytest.fixture(scope="function", autouse=True)
def before_each_after_each(page: Page):
    
    print("before the test runs")


    page.goto("https://playwright.dev/")
    yield
    
    print("after the test runs")

def test_main_navigation(page: Page):

    expect(page).to_have_url("https://playwright.dev/")