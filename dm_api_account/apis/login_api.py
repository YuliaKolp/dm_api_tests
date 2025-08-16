from restclient.client import RestClient


class LoginApi(RestClient):
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
        response = self.post(f'/v1/account/login', json=json_data)
        return response
