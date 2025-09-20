import allure
from checkers.http_checkers import check_status_code_http
from checkers.test_get_v1_account import GetV1Account


@allure.suite("Тесты на проверку метода GET v1 account")
@allure.sub_suite("Позитивные тесты")
class TestsGetV1Account:
    @allure.title("Проверка получения данных пользователя")
    def test_get_v1_account_auth(
            self,
            auth_account_helper
            ):
        response = auth_account_helper.get_user(validate_response=True)
        GetV1Account.check_response_value(response=response)

    @allure.title("Попытка получения данных пользователя без аутентификации")
    def test_get_v1_account_no_auth(
            self,
            account_helper
            ):
        with check_status_code_http(401, "User must be authenticated"):
            account_helper.get_user(validate_response=False)
