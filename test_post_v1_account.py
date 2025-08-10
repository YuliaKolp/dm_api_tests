import requests


def test_post_v1_account():
    # регистрация пользователя

    login = 'vmenshikov-test'
    password = '123456789'
    email =  f'{login} @ mail. ru'
    json_data = {
        'login': login,
        'email': email,
        'password': password,
    }

    response = requests.post('http://5.63.153.31:5051/v1/account', json=json_data)
    print(response.status_code)
    print(response.text)

    # получить письма из почтового сервера

    params = {
        'limit': '50',
    }
    response = requests.get('http://5.63.153.31:5025/api/v2/messages', params=params, verify=False)
    print(response.status_code)
    print(response.text)

    # активация пользователя
    url = 'http://5.63.153.31:5051/v1/account/f755b9d2-4ae8-4f70-9b77-8f2b66339097'

    response = requests.put(url=url)
    print(response.status_code)
    print(response.text)

    # авторизоваться

    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response = requests.post('http://5.63.153.31:5051/v1/account/login', json=json_data)
    print(response.status_code)
    print(response.text)
