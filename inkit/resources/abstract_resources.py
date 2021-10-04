from inkit.client import ClientRequest
from inkit.response_object import ResponseObject


class AbstractResource:

    _client = ClientRequest()

    __object = None
    __http_method = None
    __resource_url = None

    def make_request(self, data=None):
        resp = self._client.send(
            url=self.__resource_url,
            http_method=self.__http_method,
            data=data
        )
        return ResponseObject(**resp.josn)


class CreatableResource(AbstractResource):
    __http_method = "POST"

    def create(self, **kwargs):
        data = {
            'json': kwargs
        }
        resp_obj = self.make_request(data)
        return self.__object.build_from_resp_obj(resp_obj)


class RetrievableResource(AbstractResource):
    __http_method = "GET"


class ListableResource(AbstractResource):
    __http_method = "GET"


class UpdatableResource(AbstractResource):
    __http_method = "PATCH"


class DeletableResource(AbstractResource):
    __http_method = "DELETE"
