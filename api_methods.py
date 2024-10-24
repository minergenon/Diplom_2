import allure
import requests
from data import *


class ApiMethods:
    @staticmethod
    @allure.step("Регистрация пользователя")
    def register_user(email, password, name):
        data = {"email": email, "password": password, "name": name}
        return requests.post(Urls.REGISTER, json=data)

    @staticmethod
    @allure.step("Авторизация пользователя")
    def login_user(email, password):
        data = {"email": email, "password": password}
        return requests.post(Urls.LOGIN, json=data)

    @staticmethod
    @allure.step("Удаление пользователя")
    def delete_user(token):
        headers = {'Authorization': token}
        return requests.delete(Urls.USER, headers=headers)

    @staticmethod
    @allure.step("Изменение данных пользователя")
    def update_user(token, **data):
        headers = {'Authorization': token}
        return requests.patch(Urls.USER, json=data, headers=headers)

    @staticmethod
    @allure.step("Получение списка ингредиентов")
    def get_ingredients():
        return requests.get(Urls.INGREDIENTS)

    @staticmethod
    @allure.step("Создание заказа")
    def create_order(token, ingredients):
        headers = {'Authorization': token}
        data = {"ingredients": ingredients}
        return requests.post(Urls.ORDERS, json=data, headers=headers)

    @staticmethod
    @allure.step("Получение заказов пользователя")
    def get_user_orders(token):
        headers = {'Authorization': token}
        return requests.get(Urls.ORDERS, headers=headers)
