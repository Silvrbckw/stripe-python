# File generated from our OpenAPI spec
from __future__ import absolute_import, division, print_function

from stripe import api_requestor
from stripe import util
from stripe.api_resources.abstract import APIResourceTestHelpers
from stripe.api_resources.abstract import CreateableAPIResource
from stripe.api_resources.abstract import ListableAPIResource
from stripe.api_resources.abstract import custom_method
from stripe.api_resources.abstract import test_helpers


@test_helpers
@custom_method("cancel", http_verb="post")
class InboundTransfer(CreateableAPIResource, ListableAPIResource):
    OBJECT_NAME = "treasury.inbound_transfer"

    def cancel(self, idempotency_key=None, **params):
        return self._request(
            "post",
            "/v1/treasury/inbound_transfers/{inbound_transfer}/cancel".format(
                inbound_transfer=util.sanitize_id(self.get("id"))
            ),
            idempotency_key=idempotency_key,
            params=params,
        )

    class TestHelpers(APIResourceTestHelpers):
        @classmethod
        def _cls_fail(
            cls,
            id,
            api_key=None,
            stripe_version=None,
            stripe_account=None,
            **params
        ):
            return cls._static_request(
                "post",
                "/v1/test_helpers/treasury/inbound_transfers/{id}/fail".format(
                    id=util.sanitize_id(id)
                ),
                api_key=api_key,
                stripe_version=stripe_version,
                stripe_account=stripe_account,
                params=params,
            )

        @util.class_method_variant("_cls_fail")
        def fail(self, idempotency_key=None, **params):
            return self.resource._request(
                "post",
                "/v1/test_helpers/treasury/inbound_transfers/{id}/fail".format(
                    id=util.sanitize_id(self.get("id"))
                ),
                idempotency_key=idempotency_key,
                params=params,
            )

        @classmethod
        def _cls_return_inbound_transfer(
            cls,
            id,
            api_key=None,
            stripe_version=None,
            stripe_account=None,
            **params
        ):
            return cls._static_request(
                "post",
                "/v1/test_helpers/treasury/inbound_transfers/{id}/return".format(
                    id=util.sanitize_id(id)
                ),
                api_key=api_key,
                stripe_version=stripe_version,
                stripe_account=stripe_account,
                params=params,
            )

        @util.class_method_variant("_cls_return_inbound_transfer")
        def return_inbound_transfer(self, idempotency_key=None, **params):
            return self.resource._request(
                "post",
                "/v1/test_helpers/treasury/inbound_transfers/{id}/return".format(
                    id=util.sanitize_id(self.get("id"))
                ),
                idempotency_key=idempotency_key,
                params=params,
            )

        @classmethod
        def _cls_succeed(
            cls,
            id,
            api_key=None,
            stripe_version=None,
            stripe_account=None,
            **params
        ):
            return cls._static_request(
                "post",
                "/v1/test_helpers/treasury/inbound_transfers/{id}/succeed".format(
                    id=util.sanitize_id(id)
                ),
                api_key=api_key,
                stripe_version=stripe_version,
                stripe_account=stripe_account,
                params=params,
            )

        @util.class_method_variant("_cls_succeed")
        def succeed(self, idempotency_key=None, **params):
            return self.resource._request(
                "post",
                "/v1/test_helpers/treasury/inbound_transfers/{id}/succeed".format(
                    id=util.sanitize_id(self.get("id"))
                ),
                idempotency_key=idempotency_key,
                params=params,
            )
