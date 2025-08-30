from utils import utils


def test_put_v1_account_token(
        account_helper,
        prepare_user
        ):
    # регистрация пользователя

    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email

    account_helper.register_new_user(login=login, password=password, email=email)

    # авторизоваться без активации
    response = account_helper.user_login(login=login, password=password)
    error_message = 'User is inactive. Address the technical support for more details'
    assert response.status_code == 403, f"User cannot authorise {response.json()}"
    assert response.json()['title'] == error_message

    # активация с неверным токеном
    wrong_token_len = 7
    wrong_token = utils.generate_random_string(wrong_token_len)

    response = account_helper.dm_account_api.account_api.put_v1_account_token(token=wrong_token, validate_response=False)
    assert response.status_code == 400, f"User is activated {response.json()}"
