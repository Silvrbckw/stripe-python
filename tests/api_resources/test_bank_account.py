from __future__ import absolute_import, division, print_function

import pytest

import stripe


TEST_RESOURCE_ID = "ba_123"


class TestBankAccountTest(object):
    def construct_resource(self, **params):
        bank_dict = {
            "id": TEST_RESOURCE_ID,
            "object": "bank_account",
            "metadata": {},
        } | params
        return stripe.BankAccount.construct_from(bank_dict, stripe.api_key)

    def test_has_account_instance_url(self):
        resource = self.construct_resource(account="acct_123")
        assert (
            resource.instance_url()
            == f"/v1/accounts/acct_123/external_accounts/{TEST_RESOURCE_ID}"
        )

    def test_has_customer_instance_url(self):
        resource = self.construct_resource(customer="cus_123")
        assert (
            resource.instance_url()
            == f"/v1/customers/cus_123/sources/{TEST_RESOURCE_ID}"
        )

    # The previous tests already ensure that the request will be routed to the
    # correct URL, so we only test the API operations once.

    def test_is_not_retrievable(self):
        with pytest.raises(NotImplementedError):
            stripe.BankAccount.retrieve(TEST_RESOURCE_ID)

    def test_is_saveable(self, request_mock):
        resource = self.construct_resource(customer="cus_123")
        resource.metadata["key"] = "value"
        resource.save()
        request_mock.assert_requested(
            "post", f"/v1/customers/cus_123/sources/{TEST_RESOURCE_ID}"
        )

    def test_is_not_modifiable(self):
        with pytest.raises(NotImplementedError):
            stripe.BankAccount.modify(
                TEST_RESOURCE_ID, metadata={"key": "value"}
            )

    def test_is_deletable(self, request_mock):
        resource = self.construct_resource(customer="cus_123")
        resource.delete()
        request_mock.assert_requested(
            "delete", f"/v1/customers/cus_123/sources/{TEST_RESOURCE_ID}"
        )

    def test_is_verifiable(self, request_mock):
        resource = self.construct_resource(customer="cus_123")
        resource.verify()
        request_mock.assert_requested(
            "post", f"/v1/customers/cus_123/sources/{TEST_RESOURCE_ID}/verify"
        )
