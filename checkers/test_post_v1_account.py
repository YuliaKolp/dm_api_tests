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


class PostV1Account:
    @classmethod
    def check_response_value(
            cls,
            response,
            login_prefix="yk_test"
            ):
        today = datetime.now().strftime('%Y-%m-%d')
        assert_that(
            response, all_of(
                has_property('resource', has_property('login', starts_with(login_prefix))),
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
