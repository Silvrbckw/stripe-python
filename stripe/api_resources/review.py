# File generated from our OpenAPI spec
from __future__ import absolute_import, division, print_function

from stripe import util
from stripe.api_resources.abstract import ListableAPIResource
from stripe.api_resources.abstract import custom_method


@custom_method("approve", http_verb="post")
class Review(ListableAPIResource):
    OBJECT_NAME = "review"

    def approve(self, idempotency_key=None, **params):
        return self._request(
            "post",
            "/v1/reviews/{review}/approve".format(
                review=util.sanitize_id(self.get("id"))
            ),
            idempotency_key=idempotency_key,
            params=params,
        )
