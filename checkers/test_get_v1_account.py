from datetime import datetime

from assertpy import assert_that
from hamcrest import (
    starts_with,
    all_of,
    has_property,
    has_properties,
    equal_to,
    instance_of,
    has_items,
)

LOGIN_PREFIX = "yk_test"
class GetV1Account:
    @classmethod
    def check_response_value(
            cls,
            response
            ):

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