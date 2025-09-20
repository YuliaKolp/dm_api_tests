import allure


from checkers.http_checkers import check_status_code_http

@allure.suite("Тесты на проверку метода POST v1 account login")
@allure.sub_suite("Негативные тесты")

class TestsPostV1AccountLogin:
    @allure.title("Проверка регистрации нового пользователя")
    def test_post_v1_account_login(
            self,
            auth_account_helper,
            prepare_user
    ):
        # регистрация пользователя
        login = prepare_user.login
        password = prepare_user.password
        email = prepare_user.email

        auth_account_helper.register_and_activate_new_user(login=login, password=password, email=email)

        # авторизоваться c неверным паролем
        with check_status_code_http(400, 'One or more validation errors occurred.'):
            auth_account_helper.user_login(login=login, password=f'{password}_WRONG')
