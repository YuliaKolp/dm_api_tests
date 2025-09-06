import allure


@allure.suite("Тесты на проверку метода DELETE v1 account")
@allure.sub_suite("Позитивные тесты")
class TestsDeleteV1Account:
    # @allure.title("Проверка разлогина пользователя")
    def test_delete_v1_account_login(
            self,
            auth_account_helper
    ):
        response = auth_account_helper.dm_account_api.login_api.delete_v1_account_login()
        assert response.status_code == 204, "Cannot logout  current user"
        return response
