import pytest
import allure
from selenium.webdriver.chrome.webdriver import WebDriver
from pages import MainPage, MoviePage


@pytest.mark.ui
@allure.story("UI Кинопоиска")
class TestUI:

    @allure.title("Поиск фильма по названию")
    def test_search_movie(self, driver: WebDriver, ui_url: str) -> None:
        page = MainPage(driver, ui_url)
        page.open()
        page.search("Начало")
        with allure.step("Проверить что URL изменился на страницу поиска"):
            assert "search" in page.get_current_url(), \
                "URL не содержит 'search' после поиска"

    @allure.title("Открытие карточки фильма")
    def test_open_movie_card(self, driver: WebDriver, ui_url: str) -> None:
        page = MoviePage(driver, f"{ui_url}/film/535341/")
        page.open()
        with allure.step("Проверить что заголовок фильма не пустой"):
            assert page.get_title() != "", "Заголовок фильма пустой"

    @allure.title("Проверка рейтинга на карточке фильма")
    def test_movie_rating(self, driver: WebDriver, ui_url: str) -> None:
        page = MoviePage(driver, f"{ui_url}/film/535341/")
        page.open()
        with allure.step("Проверить что рейтинг не пустой"):
            assert page.get_rating() != "", "Рейтинг фильма пустой"

    @allure.title("Поиск актёра по имени")
    def test_search_actor(self, driver: WebDriver, ui_url: str) -> None:
        page = MainPage(driver, ui_url)
        page.open()
        page.search("Леонардо ДиКаприо")
        with allure.step("Проверить что URL изменился после поиска"):
            assert page.get_current_url() != ui_url, \
                "URL не изменился после поиска актёра"

    @allure.title("Проверка главной страницы Кинопоиска")
    def test_main_page_loads(self, driver: WebDriver, ui_url: str) -> None:
        page = MainPage(driver, ui_url)
        page.open()
        with allure.step("Проверить заголовок страницы"):
            assert "Кинопоиск" in page.get_title(), \
                "Заголовок страницы не содержит 'Кинопоиск'"
        with allure.step("Проверить что поле поиска присутствует"):
            assert page.is_search_visible(), \
                "Поле поиска не отображается на странице"
