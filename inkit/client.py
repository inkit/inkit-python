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


class Client:

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
        session.headers.update({
            'User-Agent': USER_AGENT,
            "Content-Type": "application/json"
        })
        return session

    # TODO: Public routing config map API is not implemented
    def fetch_routing_config_map(self):
        resp = self._session.get(
            url=os.path.join(HOST, PUBLIC_ROUTING_CONFIG_PATH),
            timeout=TIMEOUT
        )
        if not resp.ok:
            raise InkitClientException(
                message='API responded with invalid status code',
                resp=ResponseObject(resp)
            )
        return ResponseObject(resp)

    def send(self, path, http_method, params=None, data=None):
        if not inkit.api_token:
            raise InkitClientException(message='API Token is not specified')

        if not isinstance(inkit.api_token, str):
            raise TypeError(f'API Token must be a string, got {type(inkit.api_token)}')

        method = getattr(self._session, http_method.lower())
        request_data = {
            'url': os.path.join(HOST, path),
            'timeout': TIMEOUT,
            'headers': {'X-Inkit-API-Token': inkit.api_token}
        }
        if data:
            request_data.update(data=data)
        if params:
            request_data.update(params=params)
        try:
            resp = method(**request_data)

        except RequestException as e:
            raise InkitClientException(exc=e)

        if not resp.ok:
            raise InkitClientException(
                message='API responded with invalid status code',
                resp=ResponseObject(resp)
            )
        return ResponseObject(resp)
