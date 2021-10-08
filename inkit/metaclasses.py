import re
import inkit
import functools

from inkit.exceptions import InkitException
from inkit.response_object import ResponseObject


class ProductMetaclass(type):

    def __new__(mcs, classname, superclasses, attr_dict):
        raise InkitException(f'Class {classname} is not instantiable')

    def __getattribute__(cls, item):
        return super().__getattribute__(item)


class ResourceBuilderMetaclass(type):

    def __new__(mcs, classname, superclasses, attr_dict):
        attr_dict.update((
            (route.sdk_method_name,
             mcs.handlers_factory(http_method=route.method, resource_url=route.url))  # noqa
            for route in inkit.routing_config_map
        ))
        return super().__new__(mcs, classname, superclasses, attr_dict)

    @staticmethod
    def method_factory(resource_url, http_method):
        if re.search(r'/{id}', resource_url):
            def handler(self, entity_id, **kwargs):
                resp = self.client.send(
                    url=resource_url.format(id=entity_id),
                    http_method=http_method,
                    data=kwargs
                )
                return ResponseObject(**resp.josn)
            return handler

        else:
            def handler(self, **kwargs):
                resp = self.client.send(
                    url=resource_url,
                    http_method=http_method,
                    data=kwargs
                )
                return ResponseObject(**resp.josn)
        return handler
