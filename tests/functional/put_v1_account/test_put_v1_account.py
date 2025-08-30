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
    response = account_helper.user_login(login=login, password=password)
    assert response.status_code == 200, f"User cannot authorise {response.json()}"

    # смена email
    new_email = f'{login}_NEW@mail.ru'
    account_helper.change_account_email(login=login, password=password, new_email=new_email)

    # авторизоваться после смены пароля
    response = account_helper.user_login(login=login, password=password)
    assert response.status_code == 403, f"User can authorise after email has been altered {response.json()}"
