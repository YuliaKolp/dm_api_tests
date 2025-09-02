from checkers.http_checkers import check_status_code_http

def test_put_v1_account(
        account_helper,
        prepare_user
        ):
    # регистрация пользователя
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email

    account_helper.register_and_activate_new_user(login=login, password=password, email=email)

    # авторизоваться
    with check_status_code_http(200):
        account_helper.user_login(login=login, password=password)

    # смена email
    new_email = f'{login}_NEW@mail.ru'
    account_helper.change_account_email(login=login, password=password, new_email=new_email)

    # авторизоваться после смены email
    with check_status_code_http(403, "User is inactive. Address the technical support for more details"):
        account_helper.user_login(login=login, password=password, validate_response=False)
