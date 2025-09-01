import pytest

from checkers.http_checkers import check_status_code_http
import structlog

from utils import utils

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(
            indent=4,
            ensure_ascii=True,
            sort_keys=True
        )
    ]
)
LOGIN_PREFIX = "yk_test"
login = f'{LOGIN_PREFIX}_{utils.generate_random_string(7)}'
password = utils.generate_random_string(12)
email = f'{login}@mail.com'

short_password = '12345'  # Короткий пароль: менее 6 символов
invalid_email = f'some_email.com'  # нет символа @
short_login = 'S'  # Короткий логин
fail_status_code = 400
error_message = 'Validation failed'


@pytest.mark.parametrize(
    "login, password, email, status_code, message", [
        (login, short_password, email, fail_status_code, error_message),
        (login, password, invalid_email, fail_status_code, error_message),
        (short_login, password, email, fail_status_code, error_message),
    ]
)
def test_post_v1_account_negative(
        account_helper,
        login,
        password,
        email,
        status_code,
        message
):
    with check_status_code_http(status_code, message):
        account_helper.register_and_activate_new_user(login=login, password=password, email=email)
