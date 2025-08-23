from helpers.account_helper import AccountHelper
from utils import utils
from restclient.configuration import Configuration as DmApiConfiguration
from restclient.configuration import Configuration as MailhogConfiguration
from services.api_mailhog import MailHogApi
from services.dm_api_account import DMApiAccount



def test_put_v1_account_token():
    # регистрация пользователя

    mailhog_configuration = MailhogConfiguration(host='http://5.63.153.31:5025')
    dm_api_configuration = DmApiConfiguration(host='http://5.63.153.31:5051', disable_log=False)

    account = DMApiAccount(configuration=dm_api_configuration)
    mailhog = MailHogApi(configuration=mailhog_configuration)

    account_helper = AccountHelper(dm_account_api=account, mailhog=mailhog)

    login = utils.generate_login()
    password = '123456789'
    email = f'{login}@mail.ru'

    account_helper.register_new_user(login=login, password=password, email=email)

    # авторизоваться без активации
    response = account_helper.user_login(login=login, password=password)
    error_message = 'User is inactive. Address the technical support for more details'
    assert response.status_code == 403, f"User cannot authorise {response.json()}"
    assert response.json()['title'] == error_message

    # активация с неверным токеном
    wrong_token_len = 7
    wrong_token = utils.generate_random_string(wrong_token_len)
    response = account_helper.dm_api_account_api.account_api.put_v1_account_token(token=wrong_token)
    assert response.status_code == 400, f"User is activated {response.json()}"
