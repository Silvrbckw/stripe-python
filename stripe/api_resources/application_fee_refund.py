# -*- coding: utf-8 -*-
# File generated from our OpenAPI spec
from __future__ import absolute_import, division, print_function

from stripe import util
from stripe.api_resources import ApplicationFee
from stripe.api_resources.abstract import UpdateableAPIResource
from stripe.six.moves.urllib.parse import quote_plus


class ApplicationFeeRefund(UpdateableAPIResource):
    """
    `Application Fee Refund` objects allow you to refund an application fee that
    has previously been created but not yet refunded. Funds will be refunded to
    the Stripe account from which the fee was originally collected.

    Related guide: [Refunding application fees](https://stripe.com/docs/connect/destination-charges#refunding-app-fee)
    """

    OBJECT_NAME = "fee_refund"

    @classmethod
    def _build_instance_url(cls, fee, sid):
        fee = util.utf8(fee)
        sid = util.utf8(sid)
        base = ApplicationFee.class_url()
        cust_extn = quote_plus(fee)
        extn = quote_plus(sid)
        return f"{base}/{cust_extn}/refunds/{extn}"

    @classmethod
    def modify(cls, fee, sid, **params):
        url = cls._build_instance_url(fee, sid)
        return cls._static_request("post", url, params=params)

    def instance_url(self):
        return self._build_instance_url(self.fee, self.id)

    @classmethod
    def retrieve(cls, id, api_key=None, **params):
        raise NotImplementedError(
            "Can't retrieve a refund without an application fee ID. "
            "Use application_fee.refunds.retrieve('refund_id') instead."
        )
