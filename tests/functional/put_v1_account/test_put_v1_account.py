
from helpers.account_helper import AccountHelper
from services.api_mailhog import MailHogApi
from services.dm_api_account import DMApiAccount
from utils import utils
from restclient.configuration import Configuration as MailhogConfiguration
from restclient.configuration import Configuration as DmApiConfiguration

def test_put_v1_account():
    # регистрация пользователя

    mailhog_configuration = MailhogConfiguration(host='http://5.63.153.31:5025')
    dm_api_configuration = DmApiConfiguration(host='http://5.63.153.31:5051', disable_log=False)

    account = DMApiAccount(configuration=dm_api_configuration)
    mailhog = MailHogApi(configuration=mailhog_configuration)

    account_helper = AccountHelper(dm_account_api=account, mailhog=mailhog)

    login = utils.generate_login()
    password = '123456789'
    email = f'{login}@mail.ru'

    account_helper.register_and_activate_new_user(login=login, password=password, email=email)

    # авторизоваться
    response = account_helper.user_login(login=login, password=password)
    assert response.status_code == 200, f"User cannot authorise {response.json()}"

    # смена email
    new_email = f'{login}_NEW@mail.ru'
    account_helper.put_v1_account_email(login=login, password=password, new_email=new_email)

    # авторизоваться после смены пароля
    response = account_helper.user_login(login=login, password=password)
    assert response.status_code == 403, f"User can authorise after email has been altered {response.json()}"
