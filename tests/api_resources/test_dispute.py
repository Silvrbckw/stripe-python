from __future__ import absolute_import, division, print_function

import stripe


TEST_RESOURCE_ID = "dp_123"


class TestDispute(object):
    def test_is_listable(self, request_mock):
        resources = stripe.Dispute.list()
        request_mock.assert_requested("get", "/v1/disputes")
        assert isinstance(resources.data, list)
        assert isinstance(resources.data[0], stripe.Dispute)

    def test_is_retrievable(self, request_mock):
        resource = stripe.Dispute.retrieve(TEST_RESOURCE_ID)
        request_mock.assert_requested("get", f"/v1/disputes/{TEST_RESOURCE_ID}")
        assert isinstance(resource, stripe.Dispute)

    def test_is_saveable(self, request_mock):
        resource = stripe.Dispute.retrieve(TEST_RESOURCE_ID)
        resource.metadata["key"] = "value"
        resource.save()
        request_mock.assert_requested("post", f"/v1/disputes/{TEST_RESOURCE_ID}")

    def test_is_modifiable(self, request_mock):
        resource = stripe.Dispute.modify(
            TEST_RESOURCE_ID, metadata={"key": "value"}
        )
        request_mock.assert_requested("post", f"/v1/disputes/{TEST_RESOURCE_ID}")
        assert isinstance(resource, stripe.Dispute)

    def test_can_close(self, request_mock):
        resource = stripe.Dispute.retrieve(TEST_RESOURCE_ID)
        resource.close()
        request_mock.assert_requested("post", f"/v1/disputes/{TEST_RESOURCE_ID}/close")
        assert isinstance(resource, stripe.Dispute)

    def test_can_close_classmethod(self, request_mock):
        resource = stripe.Dispute.close(TEST_RESOURCE_ID)
        request_mock.assert_requested("post", f"/v1/disputes/{TEST_RESOURCE_ID}/close")
        assert isinstance(resource, stripe.Dispute)
