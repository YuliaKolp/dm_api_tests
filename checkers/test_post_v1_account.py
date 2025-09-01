from datetime import datetime

from assertpy import assert_that
from hamcrest import (
    starts_with,
    all_of,
    has_property,
    has_properties,
    equal_to,
    instance_of,
)

LOGIN_PREFIX = "yk_test"


class PostV1Account:
    @classmethod
    def check_response_valuse(
            cls,
            response
            ):
        today = datetime.now().strftime('%Y-%m-%d')
        assert_that(
            response, all_of(
                has_property('resource', has_property('login', starts_with(LOGIN_PREFIX))),
                has_property('resource', has_property('registration', instance_of(datetime))),
                has_property(
                    'resource', has_properties(
                        {
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
        assert_that(str(response.resource.registration), starts_with(today))
