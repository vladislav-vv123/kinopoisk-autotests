import pytest
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

SEARCH_INPUT = "input[class*='kinopoisk-header-search-form-inp']"


@pytest.mark.ui
@allure.story("UI Кинопоиска")
class TestUI:

    @allure.title("Поиск фильма по названию")
    def test_search_movie(self, driver, ui_url):
        with allure.step("Открыть главную страницу"):
            driver.get(ui_url)

        with allure.step("Найти поле поиска и ввести запрос"):
            wait = WebDriverWait(driver, 15)
            search = wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, SEARCH_INPUT)
                )
            )
            search.send_keys("Начало")
            search.send_keys(Keys.ENTER)

        with allure.step("Проверить что результаты поиска отображаются"):
            wait.until(EC.url_changes(ui_url))
            assert "search" in driver.current_url

    @allure.title("Открытие карточки фильма")
    def test_open_movie_card(self, driver, ui_url):
        with allure.step("Открыть страницу фильма"):
            driver.get(f"{ui_url}/film/535341/")

        with allure.step("Проверить что заголовок фильма отображается"):
            wait = WebDriverWait(driver, 15)
            title = wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "h1[itemprop='name']")
                )
            )
            assert title.text != ""

    @allure.title("Проверка рейтинга на карточке фильма")
    def test_movie_rating(self, driver, ui_url):
        with allure.step("Открыть страницу фильма"):
            driver.get(f"{ui_url}/film/535341/")

        with allure.step("Проверить что рейтинг отображается"):
            wait = WebDriverWait(driver, 15)
            rating = wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "span.film-rating-value")
                )
            )
            assert rating.text != ""

    @allure.title("Поиск актёра по имени")
    def test_search_actor(self, driver, ui_url):
        with allure.step("Открыть главную страницу"):
            driver.get(ui_url)

        with allure.step("Ввести имя актёра в поиск"):
            wait = WebDriverWait(driver, 15)
            search = wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, SEARCH_INPUT)
                )
            )
            search.send_keys("Леонардо ДиКаприо")
            search.send_keys(Keys.ENTER)

        with allure.step("Проверить что результаты поиска отображаются"):
            wait.until(EC.url_changes(ui_url))
            assert driver.current_url != ui_url

    @allure.title("Проверка главной страницы Кинопоиска")
    def test_main_page_loads(self, driver, ui_url):
        with allure.step("Открыть главную страницу"):
            driver.get(ui_url)

        with allure.step("Проверить заголовок страницы"):
            assert "Кинопоиск" in driver.title

        with allure.step("Проверить что поле поиска присутствует"):
            wait = WebDriverWait(driver, 15)
            search = wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, SEARCH_INPUT)
                )
            )
            assert search.is_displayed()
