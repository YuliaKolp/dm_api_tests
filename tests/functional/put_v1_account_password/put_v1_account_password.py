import allure
from utils import utils


@allure.suite("Тесты на проверку метода PUT v1 account password")
@allure.sub_suite("Позитивные тесты")
class TestsPutV1Account:
    @allure.title("Проверка смены пароля пользователя")
    def test_put_v1_account_password(
            self,
            account_helper,
            prepare_user
            ):
        # регистрация пользователя
        login = prepare_user.login
        password = prepare_user.password
        email = prepare_user.email

        account_helper.register_and_activate_new_user(login=login, password=password, email=email)

        # авторизоваться
        response = account_helper.user_login(login=login, password=password)
        assert response.status_code == 200, f"User cannot authorise {response.json()}"
        token = response.headers['X-Dm-Auth-Token']

        # смена пароля
        new_password = utils.generate_random_string(str_length=9)
        response = account_helper.change_user_password(login=login, token=token, password=password, new_password=new_password)
        assert response.status_code == 200, f"Password is not changed {response.json()}"

        # авторизоваться c новым паролем
        response = account_helper.user_login(login=login, password=new_password)
        assert response.status_code == 200, f"User cannot authorise {response.json()}"



