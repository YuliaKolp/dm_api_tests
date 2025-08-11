import requests


class AccountApi:
    def __init__(
            self,
            host,
            headers=None
    ):
        self.host = host
        self.headers = headers

    def post_v1_account(
            self,
            json_data
    ):
        """
        Register new data
        :param json_data:
        :return:
        """
        response = requests.post(
            url=f'{self.host}/v1/account',
            json=json_data
        )
        return response

    def put_v1_account_token(
            self,
            token
    ):
        """
        Activate registered user
        :param token:
        :return:
        """
        url = f'{self.host}/v1/account/{token}'
        headers = {
            'accept': 'text/plain'
        }
        response = requests.put(url=url, headers=headers)
        return response

    def put_v1_account_email(
            self,
            json_data
    ):
        """
        Change registered user email
        :param json_data:
        :return:
        """
        headers = {
            'accept': 'text/plain',
            'Content-Type': 'application/json',
        }

        url = f'{self.host}/v1/account/email'
        response = requests.put(url=url, headers=headers, json=json_data)
        return response
