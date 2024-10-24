import allure
import pytest
from api_methods import ApiMethods
from generate import generate_user_data, generate_order_data


@pytest.fixture
def create_user():
    user_data = generate_user_data()
    with allure.step("Создание тестового пользователя"):
        response = ApiMethods.register_user(**user_data)
        response.raise_for_status()  # Выбросить ошибку, если код ответа не 2xx
    yield user_data['email'], user_data['password'], user_data['name']
    with allure.step("Удаление тестового пользователя"):
        response = ApiMethods.login_user(user_data['email'], user_data['password'])
        ApiMethods.delete_user(response.json()['accessToken'])

@pytest.fixture
def new_user(create_user):
    email, password, name = create_user
    with allure.step("Получение токена авторизации"):
        login_response = ApiMethods.login_user(email, password)
        if login_response.status_code != 200:
            raise Exception(f"Не удалось получить токен. Код ответа: {login_response.status_code}")

        access_token = login_response.json().get('accessToken')
        user = {
            "email": email,
            "password": password,
            "name": name,
            "access_token": access_token
        }

    yield user

@pytest.fixture
def ingredients():
    with allure.step("Получение списка ингредиентов"):
        response = ApiMethods.get_ingredients()
        if response.status_code != 200:
            pytest.fail(f"Не удалось получить ингредиенты. Код ответа: {response.status_code}")
    return response.json()['data']

@pytest.fixture
def create_new_order(new_user, ingredients):
    def _create_order():
        order_data = generate_order_data(ingredients)
        with allure.step("Создание тестового заказа"):
            response = ApiMethods.create_order(new_user['access_token'], order_data)

        if response.status_code != 200:
            raise RuntimeError(f"Не удалось создать заказ. Код ответа: {response.status_code}")

        return response.json()

    return _create_order
