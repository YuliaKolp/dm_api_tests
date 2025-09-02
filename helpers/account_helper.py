import time
from json import loads

from dm_api_account.models.login_credentials import LoginCredentials
from dm_api_account.models.registration import Registration
from services.api_mailhog import MailHogApi
from services.dm_api_account import DMApiAccount
from retrying import retry


def retry_if_result_none(
        result
):
    """Return True if we should retry (in this case when result is None), False otherwise"""
    return result is None


def retrier(
        function
):
    def wrapper(
            *args,
            **kwargs
    ):
        token = None
        count = 0
        retry_number = 5
        while token is None:
            print(f'/****/ Попытка получения токена # {count} /****/')
            token = function(*args, **kwargs)
            count += 1
            if count == retry_number:
                raise AssertionError("Превышено количество попыток получения активационного токена")
            if token:
                return token
            time.sleep(1)

    return wrapper


class AccountHelper:
    def __init__(
            self,
            dm_account_api: DMApiAccount,
            mailhog: MailHogApi
    ):
        self.dm_account_api = dm_account_api
        self.mailhog = mailhog

    def auth_client(
            self,
            login: str,
            password: str
    ):
        response = self.user_login(login=login, password=password)

        token = {
            "x-dm-auth-token": response.headers["x-dm-auth-token"]
        }
        self.dm_account_api.account_api.set_headers(token)
        self.dm_account_api.login_api.set_headers(token)

    def register_new_user(
            self,
            login: str,
            password: str,
            email: str
    ):
        registration = Registration(
            login=login,
            email=email,
            password=password
        )

        response = self.dm_account_api.account_api.post_v1_account(registration=registration)
        assert response.status_code == 201, f"User is not created {response.json()}"

        return response

    def register_and_activate_new_user(
            self,
            login: str,
            password: str,
            email: str
    ):
        registration = Registration(
            login=login,
            email=email,
            password=password
        )

        response = self.dm_account_api.account_api.post_v1_account(registration=registration)
        assert response.status_code == 201, f"User is not created {response.json()}"

        start_time = time.time()
        token = self.get_activation_token_by_login(login=login)
        end_time = time.time()
        assert end_time - start_time < 3, "Время ожидания активации превышено"
        assert token is not None, f"No token for user {login}"

        response = self.dm_account_api.account_api.put_v1_account_token(token=token, validate_response=False)

        assert response.status_code == 200, f"User is not activated {response.json()}"
        return response

    def user_login(
            self,
            login: str,
            password: str,
            remember_me: bool = True,
            validate_response=False,
            validate_headers=False
    ):
        login_credentials = LoginCredentials(
            login=login,
            password=password,
            remember_me=remember_me
        )
        response = self.dm_account_api.login_api.post_v1_account_login(
            login_credentials=login_credentials,
            validate_response=validate_response
        )
        if validate_headers:
            assert response.headers["x-dm-auth-token"], f"Tокен не был получен"
            #assert response.status_code == 200, f"Пользователь не смог авторизоваться"
        return response

    # @retrier
    @retry(stop_max_attempt_number=5, retry_on_result=retry_if_result_none, wait_fixed=1000)
    def get_activation_token_by_login(
            self,
            login
    ):
        token = None
        response = self.mailhog.mailhog_api.get_api_v2_messages()
        for item in response.json()['items']:
            user_data = loads(item['Content']['Body'])
            user_login = user_data['Login']
            if user_login == login:
                token = user_data['ConfirmationLinkUrl'].split('/')[-1]

        return token

    def change_account_email(
            self,
            login: str,
            password: str,
            new_email: str,
            validate_response=True
    ):
        json_data = {
            'login': login,
            'password': password,
            'email': new_email,
        }

        response = self.dm_account_api.account_api.put_v1_account_email(json_data=json_data, validate_response=validate_response)
        assert response.status_code == 200, f"Email for user with login '{login}' are NOT changed. Status code is {response.status_code}"

    def change_user_password(
            self,
            login: str,
            token: str,
            password: str,
            new_password: str
    ):
        """
        Change registered user password
        :return:
        """
        headers = {
            'accept': 'text/plain',
            'Content-Type': 'application/json',
            'X-Dm-Auth-Token': token
        }

        json_data = {
            'login': login,
            'oldPassword': password,
            'newPassword': new_password
        }
        # self.dm_account_api.account_api.set_headers(token)
        response = self.dm_account_api.account_api.put_v1_account_password(headers=headers, json_data=json_data)
        return response

    def get_user(
            self,
            validate_response=False
    ):
        """
        Get current user
        :return:
        """
        response = self.dm_account_api.account_api.get_v1_account(validate_response=validate_response)
        return response
