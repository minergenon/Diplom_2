import allure
import pytest
from api_methods import ApiMethods
from expected_responses import *
from helpers import ResponseChecker


@allure.feature("Авторизация пользователя")
class TestUserLogin:

    @allure.title("Успешная авторизация существующего пользователя")
    @pytest.mark.positive
    def test_login_existing_user(self, create_user):
        email, password, _ = create_user
        response = ApiMethods.login_user(email, password)
        assert ResponseChecker.check_status_code(response, SUCCESS_CODE) and \
               ResponseChecker.check_field_exists(response, 'accessToken'), \
            f"Не удалось авторизоваться. Код ответа: {response.status_code}, тело ответа: {response.json()}"

    @allure.title("Попытка авторизации с неверными данными")
    @pytest.mark.negative
    @pytest.mark.parametrize("email,password", [
        ("wrong@email.com", "correctpassword"),
        ("correct@email.com", "wrongpassword"),
    ])

    def test_login_with_incorrect_email(self, create_user, email, password):
        correct_email, correct_password, _ = create_user
        email = "incorrect@email.com"
        password = correct_password
        response = ApiMethods.login_user(email, password)

        assert ResponseChecker.check_status_code(response, UNAUTHORIZED_CODE) and \
               ResponseChecker.check_response_field(response, 'message', LOGIN_FAILED['message']), \
            (f"Неожиданный ответ при попытке авторизации с неверным email. "
             f"Код ответа: {response.status_code}, тело ответа: {response.json()}")

    def test_login_with_incorrect_password(self, create_user):
        correct_email, correct_password, _ = create_user
        email = correct_email
        password = "incorrectpassword"
        response = ApiMethods.login_user(email, password)

        assert ResponseChecker.check_status_code(response, UNAUTHORIZED_CODE) and \
               ResponseChecker.check_response_field(response, 'message', LOGIN_FAILED['message']), \
            (f"Неожиданный ответ при попытке авторизации с неверным паролем. "
             f"Код ответа: {response.status_code}, тело ответа: {response.json()}")

    def test_login_with_both_incorrect_credentials(self, create_user):
        email = "incorrect@email.com"
        password = "incorrectpassword"
        response = ApiMethods.login_user(email, password)

        assert ResponseChecker.check_status_code(response, UNAUTHORIZED_CODE) and \
               ResponseChecker.check_response_field(response, 'message', LOGIN_FAILED['message']), \
            (f"Неожиданный ответ при попытке авторизации с неверными данными. "
             f"Код ответа: {response.status_code}, тело ответа: {response.json()}")

