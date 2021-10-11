from inkit.extensions import flat


class ResponseObject:

    def __init__(self, resp):
        self.response = resp
        self.content_type = resp.headers['content-type']
        self.status_code = resp.status_code
        self.content = resp.content
        self._json = resp.json() if self.content_type == 'application/json' else None
        self.data = flat(self._json) if self._json else None
