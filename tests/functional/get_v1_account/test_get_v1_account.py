from datetime import datetime
import structlog

from hamcrest import (
    assert_that,
    has_property,
    starts_with,
    all_of,
    instance_of,
    has_properties,
    equal_to,
    has_items,
)

from checkers.http_checkers import check_status_code_http
from checkers.test_get_v1_account import GetV1Account

LOGIN_PREFIX = "yk_test"
# from conftest import LOGIN_PREFIX

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(
            indent=4,
            ensure_ascii=True,
            sort_keys=True
        )
    ]
)


def test_get_v1_account_auth(
        auth_account_helper
):
    response = auth_account_helper.get_user(validate_response=True)

    GetV1Account.check_response_value(response)





def test_get_v1_account_no_auth(
        account_helper
):
    with check_status_code_http(401, "User must be authenticated"):
        account_helper.get_user(validate_response=False)
