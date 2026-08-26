import requests
import pytest
import allure


@pytest.mark.api
@allure.story("API Кинопоиска")
class TestApiPositive:

    @allure.title("Поиск фильма по названию")
    def test_search_movie(self, api_token, base_url):
        with allure.step("Отправить GET запрос поиска фильма"):
            response = requests.get(
                f"{base_url}/v1.4/movie/search",
                headers={"X-API-KEY": api_token},
                params={"query": "Начало", "page": 1, "limit": 5}
            )
        with allure.step("Проверить статус код 200"):
            assert response.status_code == 200
        with allure.step("Проверить что docs является массивом"):
            assert isinstance(response.json()["docs"], list)
        with allure.step("Проверить что первый результат имеет id"):
            assert "id" in response.json()["docs"][0]

    @allure.title("Получение карточки фильма по ID")
    def test_get_movie_by_id(self, api_token, base_url):
        with allure.step("Отправить GET запрос карточки фильма"):
            response = requests.get(
                f"{base_url}/v1.4/movie/535341",
                headers={"X-API-KEY": api_token}
            )
        with allure.step("Проверить статус код 200"):
            assert response.status_code == 200
        with allure.step("Проверить наличие поля name"):
            assert "name" in response.json()
        with allure.step("Проверить наличие рейтинга"):
            assert "kp" in response.json()["rating"]

    @allure.title("Поиск персоны по имени")
    def test_search_person(self, api_token, base_url):
        with allure.step("Отправить GET запрос поиска персоны"):
            response = requests.get(
                f"{base_url}/v1.4/person/search",
                headers={"X-API-KEY": api_token},
                params={"query": "Леонардо ДиКаприо", "page": 1, "limit": 5}
            )
        with allure.step("Проверить статус код 200"):
            assert response.status_code == 200
        with allure.step("Проверить что docs не пустой"):
            assert len(response.json()["docs"]) > 0
        with allure.step("Проверить наличие поля name"):
            assert "name" in response.json()["docs"][0]


@pytest.mark.api
@allure.story("API Кинопоиска")
class TestApiNegative:

    @allure.title("Запрос без токена")
    def test_no_token(self, base_url):
        with allure.step("Отправить запрос без токена"):
            response = requests.get(
                f"{base_url}/v1.4/movie/search",
                params={"query": "Начало"}
            )
        with allure.step("Проверить статус код 401"):
            assert response.status_code == 401

    @allure.title("Запрос с невалидным токеном")
    def test_invalid_token(self, base_url):
        with allure.step("Отправить запрос с невалидным токеном"):
            response = requests.get(
                f"{base_url}/v1.4/movie/search",
                headers={"X-API-KEY": "INVALID-TOKEN-00000000"},
                params={"query": "Начало"}
            )
        with allure.step("Проверить статус код 401"):
            assert response.status_code == 401

    @allure.title("Запрос с несуществующим ID фильма")
    def test_nonexistent_movie_id(self, api_token, base_url):
        with allure.step("Отправить запрос с несуществующим ID"):
            response = requests.get(
                f"{base_url}/v1.4/movie/99999999",
                headers={"X-API-KEY": api_token}
            )
        with allure.step("Проверить статус код 400 (баг: ожидался 404)"):
            assert response.status_code == 400

    @allure.title("Запрос с ID фильма строкой")
    def test_movie_id_string(self, api_token, base_url):
        with allure.step("Отправить запрос с ID строкой"):
            response = requests.get(
                f"{base_url}/v1.4/movie/abcdef",
                headers={"X-API-KEY": api_token}
            )
        with allure.step("Проверить статус код 400"):
            assert response.status_code == 400

    @allure.title("Поиск персоны со спецсимволами")
    def test_person_special_chars(self, api_token, base_url):
        with allure.step("Отправить запрос со спецсимволами"):
            response = requests.get(
                f"{base_url}/v1.4/person/search",
                headers={"X-API-KEY": api_token},
                params={"query": "!!!###"}
            )
        with allure.step("Проверить что нет 500 ошибки"):
            assert response.status_code != 500
        with allure.step("Проверить статус код 200 или 400"):
            assert response.status_code in [200, 400]
