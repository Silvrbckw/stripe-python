# File generated from our OpenAPI spec
from __future__ import absolute_import, division, print_function

from stripe import api_requestor
from stripe import util
from stripe.api_resources.abstract import APIResourceTestHelpers
from stripe.api_resources.abstract import ListableAPIResource
from stripe.api_resources.abstract import test_helpers


@test_helpers
class ReceivedDebit(ListableAPIResource):
    OBJECT_NAME = "treasury.received_debit"

    class TestHelpers(APIResourceTestHelpers):
        @classmethod
        def create(
            cls,
            api_key=None,
            stripe_version=None,
            stripe_account=None,
            **params
        ):
            return cls._static_request(
                "post",
                "/v1/test_helpers/treasury/received_debits",
                api_key=api_key,
                stripe_version=stripe_version,
                stripe_account=stripe_account,
                params=params,
            )
