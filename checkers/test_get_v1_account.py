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

class GetV1Account:
    @classmethod
    def check_response_value(
            cls,
            response,
            login_prefix="yk_test"
            ):

        assert_that(
            response, all_of(
                has_property(
                    'resource', has_properties(
                        {
                            'login': starts_with(login_prefix),
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