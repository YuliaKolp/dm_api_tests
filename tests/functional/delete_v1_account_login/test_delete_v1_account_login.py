def test_delete_v1_account_login(

        auth_account_helper
):
    response = auth_account_helper.dm_account_api.account_api.delete_v1_account_login()
    assert response.status_code == 204, "Cannot logout  current user"
    return response
