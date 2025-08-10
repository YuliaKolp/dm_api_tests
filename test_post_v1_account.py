import pprint

import requests
from json import loads

def test_post_v1_account():
    # регистрация пользователя

    login = 'yk-test'
    password = '123456789'
    email = f'{login} @ mail. ru'
    json_data = {
        'login': login,
        'email': email,
        'password': password,
    }

    response = requests.post('http://5.63.153.31:5051/v1/account', json=json_data)
    status_code = response.status_code
    print(response.text)
    assert status_code == 201, f"User is not created {response.json()}"

    # получить письма из почтового сервера

    params = {
        'limit': '50',
    }
    response = requests.get('http://5.63.153.31:5025/api/v2/messages', params=params, verify=False)
    print(response.status_code)
    status_code = response.status_code
    assert status_code == 200, f"No letters are received"

    # Получить токен
    token = None

    for item in response.json()['items']:
        user_data = loads(item['Content']['Body'])
        user_login = user_data['Login']

        if user_login == login:
            print(user_login)
            token = user_data['ConfirmationLinkUrl'].split('/')[-1]
            print(token)
    assert token is not None, f"No token for user {login}"

    # активация пользователя
    url = f'http://5.63.153.31:5051/v1/account/{token}'

    response = requests.put(url=url)
    print(response.status_code)
    print(response.text)
    assert status_code == 200, f"User is not activated {response.json()}"

    # авторизоваться

    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response = requests.post('http://5.63.153.31:5051/v1/account/login', json=json_data)
    print(response.status_code)
    print(response.text)
    assert status_code == 200, f"User cannot authorise {response.json()}"
