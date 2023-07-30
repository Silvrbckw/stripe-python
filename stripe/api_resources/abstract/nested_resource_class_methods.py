from __future__ import absolute_import, division, print_function

from stripe.six.moves.urllib.parse import quote_plus

from stripe.api_resources.abstract import APIResource


def nested_resource_class_methods(
    resource, path=None, operations=None, resource_plural=None
):
    if resource_plural is None:
        resource_plural = f"{resource}s"
    if path is None:
        path = resource_plural
    if operations is None:
        raise ValueError("operations list required")

    def wrapper(cls):
        def nested_resource_url(cls, id, nested_id=None):
            url = f"{cls.class_url()}/{quote_plus(id)}/{quote_plus(path)}"
            if nested_id is not None:
                url += f"/{quote_plus(nested_id)}"
            return url

        resource_url_method = f"{resource}s_url"
        setattr(cls, resource_url_method, classmethod(nested_resource_url))

        def nested_resource_request(
            cls,
            method,
            url,
            api_key=None,
            idempotency_key=None,
            stripe_version=None,
            stripe_account=None,
            **params
        ):
            return APIResource._static_request(
                method,
                url,
                api_key=api_key,
                idempotency_key=idempotency_key,
                stripe_version=stripe_version,
                stripe_account=stripe_account,
                params=params,
            )

        resource_request_method = f"{resource}s_request"
        setattr(
            cls, resource_request_method, classmethod(nested_resource_request)
        )

        for operation in operations:
            if operation == "create":

                def create_nested_resource(cls, id, **params):
                    url = getattr(cls, resource_url_method)(id)
                    return getattr(cls, resource_request_method)(
                        "post", url, **params
                    )

                create_method = f"create_{resource}"
                setattr(
                    cls, create_method, classmethod(create_nested_resource)
                )

            elif operation == "retrieve":

                def retrieve_nested_resource(cls, id, nested_id, **params):
                    url = getattr(cls, resource_url_method)(id, nested_id)
                    return getattr(cls, resource_request_method)(
                        "get", url, **params
                    )

                retrieve_method = f"retrieve_{resource}"
                setattr(
                    cls, retrieve_method, classmethod(retrieve_nested_resource)
                )

            elif operation == "update":

                def modify_nested_resource(cls, id, nested_id, **params):
                    url = getattr(cls, resource_url_method)(id, nested_id)
                    return getattr(cls, resource_request_method)(
                        "post", url, **params
                    )

                modify_method = f"modify_{resource}"
                setattr(
                    cls, modify_method, classmethod(modify_nested_resource)
                )

            elif operation == "delete":

                def delete_nested_resource(cls, id, nested_id, **params):
                    url = getattr(cls, resource_url_method)(id, nested_id)
                    return getattr(cls, resource_request_method)(
                        "delete", url, **params
                    )

                delete_method = f"delete_{resource}"
                setattr(
                    cls, delete_method, classmethod(delete_nested_resource)
                )

            elif operation == "list":

                def list_nested_resources(cls, id, **params):
                    url = getattr(cls, resource_url_method)(id)
                    return getattr(cls, resource_request_method)(
                        "get", url, **params
                    )

                list_method = f"list_{resource_plural}"
                setattr(cls, list_method, classmethod(list_nested_resources))

            else:
                raise ValueError(f"Unknown operation: {operation}")

        return cls

    return wrapper
