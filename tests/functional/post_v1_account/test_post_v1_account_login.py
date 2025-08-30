import structlog

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(
            indent=4,
            ensure_ascii=True,
            sort_keys=True
        )
    ]
)


def test_post_v1_account_login(
        auth_account_helper,
        prepare_user
):
    # регистрация пользователя
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email

    auth_account_helper.register_and_activate_new_user(login=login, password=password, email=email)

    # авторизоваться c неверным паролем
    response = auth_account_helper.user_login(login=login, password=f'{password}_WRONG')
    assert response.status_code == 400, (f"User cannot authorise!{response.json()}")
