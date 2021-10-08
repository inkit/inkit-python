from collections import namedtuple
Route = namedtuple('Route', ['name', 'url', 'method', 'sdk_method_name'])
routing_config_map = [Route('rendersCreate', 'http://renders-create', 'POST', 'create'), Route('rendersRetrieve', 'http://renders-retrieve', 'GET', 'get')]


class ResourceBuilderMetaclass(type):

    def __new__(mcs, classname, superclasses, attr_dict):
        attr_dict.update((
            (route.sdk_method_name,
             mcs.method_factory(http_method=route.method, resource_url=route.url))  # noqa
            for route in routing_config_map
        ))
        return super().__new__(mcs, classname, superclasses, attr_dict)

    @staticmethod
    def method_factory(http_method, resource_url):
        def make_request(self, data):
            print(f'class {isinstance(self, RenderResource)} - method:{http_method} - resource_url: {resource_url}')
            return 'LOL'
        return make_request


class RenderResource(metaclass=ResourceBuilderMetaclass):
    pass


render = RenderResource()
