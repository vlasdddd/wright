# ФИО: Зубов Владислав Витальевич
# Дата: 2026-11-14
# Время: 12:07
# Описание модификации:
# Вместо одного фрукта теперь передаётся список из двух элементов (Strawberry и Mango), а также явно указан HTTP-статус status=200.
# Добавлена проверка видимости второго фрукта (Mango) и негативная проверка (not_to_be_visible), которая гарантирует, что реальные данные с сервера не просочились на страницу.

import pytest
from playwright.sync_api import Page, Route, expect


# Объявляем тестовую функцию, которая принимает объект страницы браузера (page)
def test_mock_the_fruit_api(page: Page):
    # Создаём функцию-обработчик для перехваченного сетевого запроса (route)
    def handle(route: Route):
        # Подготавливаем поддельные (моковые) данные: добавили второй фрукт для проверки списка
        mock_data = [
            {"name": "Strawberry", "id": 21},
            {"name": "Mango", "id": 22},
        ]
        # Отвечаем на перехваченный запрос нашими данными со статусом 200 (Успешно)
        route.fulfill(status=200, json=mock_data)

    # Включаем перехват всех запросов по маске адреса "*/**/api/v1/fruits" и передаём их в функцию handle
    page.route("*/**/api/v1/fruits", handle)

    # Открываем в браузере правильную демо-страницу
    url = "https://demo." + "playwright.dev/api-mocking"
    page.goto(url)


    # Проверяем, что оба наших поддельных фрукта появились и стали видимыми на странице
    expect(page.get_by_text("Strawberry")).to_be_visible()
    expect(page.get_by_text("Mango")).to_be_visible()

    # Дополнительная проверка: убеждаемся, что реальный фрукт с сервера ("Banana") не отобразился
    expect(page.get_by_text("Banana")).not_to_be_visible()


if __name__ == "__main__":
    pytest.main(["-v", __file__])

