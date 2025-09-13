import allure
import pytest

from checkers.http_checkers import check_status_code_http
from utils import utils

#@pytest.mark.skip
@allure.suite("Тесты на проверку метода PUT v1 account token")
@allure.sub_suite("Негативные тесты")
class TestsPutV1AccountToken:
    @allure.title("Проверка невозможности активации с неверным токеном")
    def test_put_v1_account_token(
            self,
            account_helper,
            prepare_user
            ):
        # регистрация пользователя

        login = prepare_user.login
        password = prepare_user.password
        email = prepare_user.email

        account_helper.register_new_user(login=login, password=password, email=email)

        # авторизоваться без активации
        with check_status_code_http(403, "User is inactive. Address the technical support for more details"):
            account_helper.user_login(login=login, password=password, validate_response=False)

        # активация с неверным токеном
        wrong_token_len = 7
        wrong_token = utils.generate_random_string(wrong_token_len)

        with check_status_code_http(400, 'One or more validation errors occurred.'):
            account_helper.dm_account_api.account_api.put_v1_account_token(token=wrong_token, validate_response=False)
