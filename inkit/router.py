import os
import json

from collections import namedtuple

from inkit.exceptions import InkitRouterException


ROUTING_CONFIG_MAP_FILENAME = os.path.join(
    os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))),
    'routing-config-map.json'
)


Route = namedtuple('Route', ['path', 'http_method', 'sdk_method_name', 'doc'])


class Router:

    with open(ROUTING_CONFIG_MAP_FILENAME) as fp:
        config_map = json.load(fp)

    @classmethod
    def get_routes(cls, product_name):
        routes = [
            Route(path=route['path'],
                  sdk_method_name=route['sdk_method_name'],
                  http_method=route['http_method'],
                  doc=route['doc'])
            for route in cls.config_map[product_name]['routes']
        ]
        if not routes:
            raise InkitRouterException(
                message=f'Routes not found for product {product_name}'
            )

        return routes
