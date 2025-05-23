from __future__ import absolute_import, division, print_function

from stripe import six, util
from stripe.stripe_object import StripeObject

from stripe.six.moves.urllib.parse import quote_plus


class ListObject(StripeObject):
    OBJECT_NAME = "list"

    def list(
        self, api_key=None, stripe_version=None, stripe_account=None, **params
    ):
        return self._request(
            "get",
            self.get("url"),
            api_key=api_key,
            stripe_version=stripe_version,
            stripe_account=stripe_account,
            params=params,
        )

    def create(
        self,
        api_key=None,
        idempotency_key=None,
        stripe_version=None,
        stripe_account=None,
        **params
    ):
        return self._request(
            "post",
            self.get("url"),
            api_key=api_key,
            idempotency_key=idempotency_key,
            stripe_version=stripe_version,
            stripe_account=stripe_account,
            params=params,
        )

    def retrieve(
        self,
        id,
        api_key=None,
        stripe_version=None,
        stripe_account=None,
        **params
    ):
        url = f'{self.get("url")}/{quote_plus(util.utf8(id))}'
        return self._request(
            "get",
            url,
            api_key=api_key,
            stripe_version=stripe_version,
            stripe_account=stripe_account,
            params=params,
        )

    def __getitem__(self, k):
        if isinstance(k, six.string_types):
            return super(ListObject, self).__getitem__(k)
        else:
            raise KeyError(
                "You tried to access the %s index, but ListObject types only "
                "support string keys. (HINT: List calls return an object with "
                "a 'data' (which is the data array). You likely want to call "
                ".data[%s])" % (repr(k), repr(k))
            )

    def __iter__(self):
        return getattr(self, "data", []).__iter__()

    def __len__(self):
        return getattr(self, "data", []).__len__()

    def __reversed__(self):
        return getattr(self, "data", []).__reversed__()

    def auto_paging_iter(self):
        page = self

        while True:
            if (
                "ending_before" in self._retrieve_params
                and "starting_after" not in self._retrieve_params
            ):
                yield from reversed(page)
                page = page.previous_page()
            else:
                yield from page
                page = page.next_page()

            if page.is_empty:
                break

    @classmethod
    def empty_list(
        cls, api_key=None, stripe_version=None, stripe_account=None
    ):
        return cls.construct_from(
            {"data": []},
            key=api_key,
            stripe_version=stripe_version,
            stripe_account=stripe_account,
            last_response=None,
        )

    @property
    def is_empty(self):
        return not self.data

    def next_page(
        self, api_key=None, stripe_version=None, stripe_account=None, **params
    ):
        if not self.has_more:
            return self.empty_list(
                api_key=api_key,
                stripe_version=stripe_version,
                stripe_account=stripe_account,
            )

        last_id = self.data[-1].id

        params_with_filters = self._retrieve_params.copy()
        params_with_filters.update({"starting_after": last_id})
        params_with_filters.update(params)

        return self.list(
            api_key=api_key,
            stripe_version=stripe_version,
            stripe_account=stripe_account,
            **params_with_filters
        )

    def previous_page(
        self, api_key=None, stripe_version=None, stripe_account=None, **params
    ):
        if not self.has_more:
            return self.empty_list(
                api_key=api_key,
                stripe_version=stripe_version,
                stripe_account=stripe_account,
            )

        first_id = self.data[0].id

        params_with_filters = self._retrieve_params.copy()
        params_with_filters.update({"ending_before": first_id})
        params_with_filters.update(params)

        return self.list(
            api_key=api_key,
            stripe_version=stripe_version,
            stripe_account=stripe_account,
            **params_with_filters
        )
