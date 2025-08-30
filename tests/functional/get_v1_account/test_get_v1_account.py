from datetime import datetime

import structlog

from conftest import LOGIN_PREFIX

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(
            indent=4,
            ensure_ascii=True,
            sort_keys=True
        )
    ]
)

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


def test_get_v1_account_auth(
        auth_account_helper
):
    response = auth_account_helper.get_user(validate_response=True)

    assert_that(
        response, all_of(
            has_property(
                'resource', has_properties(
                    {
                        'login': starts_with(LOGIN_PREFIX),
                        'online': instance_of(datetime),
                        'registration': instance_of(datetime),
                        'roles': has_items("Guest", "Player"),
                        'rating': has_properties(
                            {
                                "enabled": equal_to(True),
                                "quality": equal_to(0),
                                "quantity": equal_to(0)
                            }
                        )
                    }
                )
            )

        )

    )

    def test_get_v1_account_no_auth(
            account_helper
    ):
        response = account_helper.get_user(validate_response=False)
        assert response.status_code == 401, "Can get user account"
