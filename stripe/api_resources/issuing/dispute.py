# File generated from our OpenAPI spec
from __future__ import absolute_import, division, print_function

from stripe import util
from stripe.api_resources.abstract import CreateableAPIResource
from stripe.api_resources.abstract import ListableAPIResource
from stripe.api_resources.abstract import UpdateableAPIResource
from stripe.api_resources.abstract import custom_method


@custom_method("submit", http_verb="post")
class Dispute(
    CreateableAPIResource,
    ListableAPIResource,
    UpdateableAPIResource,
):
    OBJECT_NAME = "issuing.dispute"

    def submit(self, idempotency_key=None, **params):
        return self._request(
            "post",
            "/v1/issuing/disputes/{dispute}/submit".format(
                dispute=util.sanitize_id(self.get("id"))
            ),
            idempotency_key=idempotency_key,
            params=params,
        )
