import allure
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

SEARCH_INPUT = "input[class*='kinopoisk-header-search-form-inp']"


class MainPage:

    def __init__(self, driver: WebDriver, url: str) -> None:
        self.driver = driver
        self.url = url
        self.wait = WebDriverWait(driver, 15)

    @allure.step("Открыть главную страницу")
    def open(self) -> None:
        self.driver.get(self.url)

    @allure.step("Ввести запрос в поиск и нажать Enter")
    def search(self, query: str) -> None:
        search = self.wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, SEARCH_INPUT)
            )
        )
        search.send_keys(query)
        search.send_keys(Keys.ENTER)

    @allure.step("Получить текущий URL")
    def get_current_url(self) -> str:
        self.wait.until(EC.url_changes(self.url))
        return self.driver.current_url

    @allure.step("Получить заголовок страницы")
    def get_title(self) -> str:
        return self.driver.title

    @allure.step("Проверить что поле поиска отображается")
    def is_search_visible(self) -> bool:
        search = self.wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, SEARCH_INPUT)
            )
        )
        return search.is_displayed()


class MoviePage:

    def __init__(self, driver: WebDriver, url: str) -> None:
        self.driver = driver
        self.url = url
        self.wait = WebDriverWait(driver, 15)

    @allure.step("Открыть страницу фильма")
    def open(self) -> None:
        self.driver.get(self.url)

    @allure.step("Получить заголовок фильма")
    def get_title(self) -> str:
        title = self.wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "h1[itemprop='name']")
            )
        )
        return title.text

    @allure.step("Получить рейтинг фильма")
    def get_rating(self) -> str:
        rating = self.wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "span.film-rating-value")
            )
        )
        return rating.text
