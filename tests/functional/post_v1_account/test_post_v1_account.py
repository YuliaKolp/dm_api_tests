from checkers.test_post_v1_account import PostV1Account

def test_post_v1_account(
        account_helper,
        prepare_user
):
    # регистрация пользователя
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email
    account_helper.register_and_activate_new_user(login=login, password=password, email=email)
    # авторизоваться
    response = account_helper.user_login(login=login, password=password, validate_response=True)
    PostV1Account.check_response_value(response)
