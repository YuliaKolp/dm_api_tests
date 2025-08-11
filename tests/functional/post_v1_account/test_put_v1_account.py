from json import loads

from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi
from api_mailhog.apis.mailhog_api import MailhogApi
from utils import utils


def test_put_v1_account():
    # регистрация пользователя
    account_api = AccountApi(host='http://5.63.153.31:5051')
    login_api = LoginApi(host='http://5.63.153.31:5051')
    mailhog_api = MailhogApi(host='http://5.63.153.31:5025')
    login = utils.generate_login()
    password = '123456789'
    email_postfix = '@mail.ru'
    email = f'{login}{email_postfix}'
    json_data = {
        'login': login,
        'email': email,
        'password': password,
    }

    response = account_api.post_v1_account(json_data=json_data)
    status_code = response.status_code
    assert status_code == 201, f"User is not created {response.json()}"

    # получить письма из почтового сервера

    response = mailhog_api.get_api_v2_messages()
    print(f'{response.status_code}')
    status_code = response.status_code
    assert status_code == 200, f"No letters are received. Status code is {status_code}"

    # Получить токен
    token = get_activation_token_by_login(login, response)
    status_code = response.status_code
    assert token is not None, f"No token for user {login}"

    # активация пользователя
    response = account_api.put_v1_account_token(token=token)
    status_code = response.status_code
    assert status_code == 200, f"User is not activated {response.json()}"

    # смена email
    new_email = f'{login}_NEW{email_postfix}'
    json_data = {
        'login': login,
        'password': password,
        'email': new_email,
    }

    response = account_api.put_v1_account_email(json_data=json_data)
    status_code = response.status_code
    assert status_code == 200, f"Email for user with login '{login}' are NOT changed. Status code is {status_code}"

    # авторизоваться со старым токеном
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }
    response = login_api.post_v1_account_login(json_data=json_data)
    status_code = response.status_code
    assert status_code == 403, f"User can authorise after email has been altered {response.json()}"

    # получить письма из почтового сервера с измененным email

    response = mailhog_api.get_api_v2_messages()
    status_code = response.status_code
    assert status_code == 200, f"No letters are received. Status code is {status_code}"

    # Получить токен
    token = get_activation_token_by_login(login, response)
    assert token is not None, f"No token for user {login}"

    # активация пользователя
    response = account_api.put_v1_account_token(token=token)
    status_code = response.status_code
    assert status_code == 200, f"User is not activated after email change {response.json()}"

    # авторизоваться после смены емейла
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }
    response = login_api.post_v1_account_login(json_data=json_data)
    status_code = response.status_code
    assert status_code == 200, f"User cannot authorise {response.json()}"


def get_activation_token_by_login(
        login,
        response
):
    token = None
    for item in response.json()['items']:
        user_data = loads(item['Content']['Body'])
        user_login = user_data['Login']
        if user_login == login:
            token = user_data['ConfirmationLinkUrl'].split('/')[-1]

    return token
