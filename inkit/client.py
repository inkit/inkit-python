import os
import requests

from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from requests.exceptions import RequestException

import inkit
from inkit.response_object import ResponseObject
from inkit.exceptions import InkitClientException


HOST = 'https://api.inkit.com/v1'
PUBLIC_ROUTING_CONFIG_PATH = 'public-routing-config-map'
USER_AGENT = 'Inkit SDK'
MAX_RETRIES = 3
TIMEOUT = 10


class ClientRequest:

    def __init__(self):
        self._session = self._build_session()

    @staticmethod
    def _build_session():
        session = requests.Session()
        retries = Retry(
            total=MAX_RETRIES,
            backoff_factor=0.1,
            status_forcelist=[500]
        )
        session.mount(HOST, HTTPAdapter(max_retries=retries))
        session.headers.update({'User-Agent': USER_AGENT})
        return session

    def fetch_routing_config_map(self):
        resp = self._session.get(
            url=os.path.join(HOST, PUBLIC_ROUTING_CONFIG_PATH),
            timeout=TIMEOUT
        )
        if not resp.ok:
            raise InkitClientException(f'Received {resp.status_code} status code, data: {resp.text}')

        return ResponseObject(**resp.json())

    def send(self, url, http_method, data=None):

        if not inkit.api_token:
            raise InkitClientException('API Token is not specified')

        if not isinstance(inkit.api_token, str):
            raise TypeError(f'API Token must be a string, got {type(inkit.api_token)}')

        method = getattr(self._session, http_method)

        rq_kwargs = {
            'url': url,
            'timeout': TIMEOUT,
            'headers': {'X-Inkit-API-Token': inkit.api_token}
        }
        if data:
            rq_kwargs.update(data)

        try:
            resp = method(**rq_kwargs)

        except RequestException as e:
            raise InkitClientException(original_exc=e)

        if not resp.ok:
            raise InkitClientException(f'Received {resp.status_code} status code, data: {resp.text}')

        return ResponseObject(**resp.json())

    def _build_url(self, chain, entity_id):
        url = '{host}/{chain}'.format(
            host=self.host,
            chain='-'.join(chain.lower().split('.'))
        )
        if entity_id:
            url += '/{}'.format(entity_id)
        return url
