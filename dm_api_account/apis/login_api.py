import requests


class LoginApi:
    def __init__(
            self,
            host,
            headers=None
    ):
        self.host = host
        self.headers = headers


    def post_v1_account_login(
            self,
            json_data
            ):
        """
        Authenticate via credentials
        :param self:
        :param json_data:
        :param login:
        :param password:
        :return:
        """
        response = requests.post(f'{self.host}/v1/account/login', json=json_data)
        return response
