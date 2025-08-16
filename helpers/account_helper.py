from json import loads

from services.api_mailhog import MailHogApi
from services.dm_api_account import DMApiAccount
from utils import utils


class AccountHelper:
    def __init__(
            self,
            dm_account_api: DMApiAccount,
            mailhog: MailHogApi
    ):
        self.dm_api_account_api = dm_account_api
        self.mailhog = mailhog

    def register_new_user(
            self,
            login: str,
            password: str,
            email: str
    ):
        json_data = {
            'login': login,
            'email': email,
            'password': password,
        }

        response = self.dm_api_account_api.account_api.post_v1_account(json_data=json_data)
        assert response.status_code == 201, f"User is not created {response.json()}"
        response = self.mailhog.mailhog_api.get_api_v2_messages()
        assert response.status_code == 200, f"No letters are received. Status code is {response.status_code}"
        token = self.get_activation_token_by_login(login=login, response=response)
        assert token is not None, f"No token for user {login}"
        response = self.dm_api_account_api.account_api.put_v1_account_token(token=token)
        assert response.status_code == 200, f"User is not activated {response.json()}"
        return response

    def user_login(
            self,
            login: str,
            password: str,
            remember_me: bool = True
    ):
        json_data = {
            'login': login,
            'password': password,
            'rememberMe': remember_me,
        }
        response = self.dm_api_account_api.login_api.post_v1_account_login(json_data=json_data)
        assert response.status_code == 200, f"User cannot authorise {response.json()}"
        return response

    # Костыль - Не знаю, как красиво переопределить (?) метод user_login
    def user_login_wrong_password(
            self,
            login: str,
            password: str
    ):
        wrong_password = utils.generate_random_string(len(password))  # try to use password of the same length
        json_data = {
            'login': login,
            'password': wrong_password,
            'rememberMe': True,
        }
        response = self.dm_api_account_api.login_api.post_v1_account_login(json_data=json_data)
        assert response.status_code == 400, f"User can authorise with wrong password {response.json()}"
        return response

    @staticmethod
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
