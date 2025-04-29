from __future__ import absolute_import, division, print_function

import stripe


TEST_RESOURCE_ID = "cus_123"
TEST_SUB_ID = "sub_123"
TEST_SOURCE_ID = "ba_123"
TEST_TAX_ID_ID = "txi_123"
TEST_TRANSACTION_ID = "cbtxn_123"


class TestCustomer(object):
    def test_is_listable(self, request_mock):
        resources = stripe.Customer.list()
        request_mock.assert_requested("get", "/v1/customers")
        assert isinstance(resources.data, list)
        assert isinstance(resources.data[0], stripe.Customer)

    def test_is_retrievable(self, request_mock):
        resource = stripe.Customer.retrieve(TEST_RESOURCE_ID)
        request_mock.assert_requested("get", f"/v1/customers/{TEST_RESOURCE_ID}")
        assert isinstance(resource, stripe.Customer)

    def test_is_creatable(self, request_mock):
        resource = stripe.Customer.create()
        request_mock.assert_requested("post", "/v1/customers")
        assert isinstance(resource, stripe.Customer)

    def test_is_saveable(self, request_mock):
        resource = stripe.Customer.retrieve(TEST_RESOURCE_ID)
        resource.metadata["key"] = "value"
        resource.save()
        request_mock.assert_requested("post", f"/v1/customers/{TEST_RESOURCE_ID}")

    def test_is_modifiable(self, request_mock):
        resource = stripe.Customer.modify(
            TEST_RESOURCE_ID, metadata={"key": "value"}
        )
        request_mock.assert_requested("post", f"/v1/customers/{TEST_RESOURCE_ID}")
        assert isinstance(resource, stripe.Customer)

    def test_is_deletable(self, request_mock):
        resource = stripe.Customer.retrieve(TEST_RESOURCE_ID)
        resource.delete()
        request_mock.assert_requested("delete", f"/v1/customers/{TEST_RESOURCE_ID}")
        assert resource.deleted is True

    def test_can_delete(self, request_mock):
        resource = stripe.Customer.delete(TEST_RESOURCE_ID)
        request_mock.assert_requested("delete", f"/v1/customers/{TEST_RESOURCE_ID}")
        assert resource.deleted is True

    def test_can_delete_discount(self, request_mock):
        resource = stripe.Customer.retrieve(TEST_RESOURCE_ID)
        resource.delete_discount()
        request_mock.assert_requested(
            "delete", f"/v1/customers/{TEST_RESOURCE_ID}/discount"
        )

    def test_can_delete_discount_class_method(self, request_mock):
        stripe.Customer.delete_discount(TEST_RESOURCE_ID)
        request_mock.assert_requested(
            "delete", f"/v1/customers/{TEST_RESOURCE_ID}/discount"
        )


class TestCustomerSources(object):
    def test_is_creatable(self, request_mock):
        stripe.Customer.create_source(TEST_RESOURCE_ID, source="btok_123")
        request_mock.assert_requested(
            "post", f"/v1/customers/{TEST_RESOURCE_ID}/sources"
        )

    def test_is_retrievable(self, request_mock):
        stripe.Customer.retrieve_source(TEST_RESOURCE_ID, TEST_SOURCE_ID)
        request_mock.assert_requested(
            "get", f"/v1/customers/{TEST_RESOURCE_ID}/sources/{TEST_SOURCE_ID}"
        )

    def test_is_modifiable(self, request_mock):
        stripe.Customer.modify_source(
            TEST_RESOURCE_ID, TEST_SOURCE_ID, metadata={"foo": "bar"}
        )
        request_mock.assert_requested(
            "post", f"/v1/customers/{TEST_RESOURCE_ID}/sources/{TEST_SOURCE_ID}"
        )

    def test_is_deletable(self, request_mock):
        stripe.Customer.delete_source(TEST_RESOURCE_ID, TEST_SOURCE_ID)
        request_mock.assert_requested(
            "delete", f"/v1/customers/{TEST_RESOURCE_ID}/sources/{TEST_SOURCE_ID}"
        )

    def test_is_listable(self, request_mock):
        resources = stripe.Customer.list_sources(TEST_RESOURCE_ID)
        request_mock.assert_requested(
            "get", f"/v1/customers/{TEST_RESOURCE_ID}/sources"
        )
        assert isinstance(resources.data, list)


class TestCustomerTaxIds(object):
    def test_is_creatable(self, request_mock):
        resource = stripe.Customer.create_tax_id(
            TEST_RESOURCE_ID, type="eu_vat", value="11111"
        )
        request_mock.assert_requested(
            "post", f"/v1/customers/{TEST_RESOURCE_ID}/tax_ids"
        )
        assert isinstance(resource, stripe.TaxId)

    def test_is_retrievable(self, request_mock):
        stripe.Customer.retrieve_tax_id(TEST_RESOURCE_ID, TEST_TAX_ID_ID)
        request_mock.assert_requested(
            "get", f"/v1/customers/{TEST_RESOURCE_ID}/tax_ids/{TEST_TAX_ID_ID}"
        )

    def test_is_deletable(self, request_mock):
        stripe.Customer.delete_tax_id(TEST_RESOURCE_ID, TEST_TAX_ID_ID)
        request_mock.assert_requested(
            "delete", f"/v1/customers/{TEST_RESOURCE_ID}/tax_ids/{TEST_TAX_ID_ID}"
        )

    def test_is_listable(self, request_mock):
        resources = stripe.Customer.list_tax_ids(TEST_RESOURCE_ID)
        request_mock.assert_requested(
            "get", f"/v1/customers/{TEST_RESOURCE_ID}/tax_ids"
        )
        assert isinstance(resources.data, list)


class TestCustomerTransactions(object):
    def test_is_creatable(self, request_mock):
        resource = stripe.Customer.create_balance_transaction(
            TEST_RESOURCE_ID, amount=1234, currency="usd"
        )
        request_mock.assert_requested(
            "post", f"/v1/customers/{TEST_RESOURCE_ID}/balance_transactions"
        )
        assert isinstance(resource, stripe.CustomerBalanceTransaction)

    def test_is_retrievable(self, request_mock):
        stripe.Customer.retrieve_balance_transaction(
            TEST_RESOURCE_ID, TEST_TRANSACTION_ID
        )
        request_mock.assert_requested(
            "get",
            f"/v1/customers/{TEST_RESOURCE_ID}/balance_transactions/{TEST_TRANSACTION_ID}",
        )

    def test_is_listable(self, request_mock):
        resources = stripe.Customer.list_balance_transactions(TEST_RESOURCE_ID)
        request_mock.assert_requested(
            "get", f"/v1/customers/{TEST_RESOURCE_ID}/balance_transactions"
        )
        assert isinstance(resources.data, list)


class TestCustomerPaymentMethods(object):
    def test_is_listable(self, request_mock):
        stripe.Customer.list_payment_methods(TEST_RESOURCE_ID, type="card")
        request_mock.assert_requested(
            "get", f"/v1/customers/{TEST_RESOURCE_ID}/payment_methods"
        )

    def test_is_listable_on_object(self, request_mock):
        resource = stripe.Customer.retrieve(
            TEST_RESOURCE_ID
        ).list_payment_methods(TEST_RESOURCE_ID, type="card")
        request_mock.assert_requested(
            "get", f"/v1/customers/{TEST_RESOURCE_ID}/payment_methods"
        )
        assert isinstance(resource, stripe.ListObject)


class TestCustomerCashBalanceMethods(object):
    # These tests are present for compatibility purposes. Previously the cash
    # balance methods required None as a second nested_id parameter. The method
    # has been patched to no longer require this, but we want to preserve
    # compatibility for existing users.
    def test_customer_cashbalance_retrieve_legacy_call_pattern(
        self, request_mock
    ):
        stripe.Customer.retrieve_cash_balance("cus_123", None)
        request_mock.assert_requested(
            "get", "/v1/customers/cus_123/cash_balance"
        )

    def test_customer_cashbalance_modify_legacy_call_pattern(
        self, request_mock
    ):
        stripe.Customer.modify_cash_balance(
            "cus_123",
            None,
            settings={"reconciliation_mode": "manual"},
        )
        request_mock.assert_requested(
            "post",
            "/v1/customers/cus_123/cash_balance",
            {"settings": {"reconciliation_mode": "manual"}},
        )

    def test_customer_cashbalance_modify_fixed_pattern(self, request_mock):
        stripe.Customer.modify_cash_balance(
            "cus_123",
            settings={"reconciliation_mode": "manual"},
        )
        request_mock.assert_requested(
            "post",
            "/v1/customers/cus_123/cash_balance",
            {"settings": {"reconciliation_mode": "manual"}},
        )
