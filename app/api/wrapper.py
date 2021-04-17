import base64
import random
import uuid
from hashlib import sha1
import hmac
import requests
import hashlib
from urllib.parse import urlencode
from time import time
from django.conf import settings

session = requests.session()
CONNECT_TIMEOUT = 3.5
READ_TIMEOUT = 9999


class CasinoSlots:
    BASE_URL = 'https://staging.gamerouter.pw/api/index.php/v1'

    def __init__(self, merch_id, merch_key):
        self.merch_id = merch_id
        self.merch_key = merch_key

    def _make_signature(self, params, headers):
        sorted_dict = dict(sorted({**params, **headers}.items()))
        string_from_dict = urlencode(sorted_dict)
        hashed = hmac.new(base64.b64decode(self.merch_key), base64.b64decode(string_from_dict), sha1)
        hashed = hashed.digest()
        return str(base64.urlsafe_b64encode(hashed), 'UTF-8')

    def _request(self, endpoint, method='get', params=None, data=None, proxy=None):
        nonce = uuid.uuid4().hex
        headers = {
            'X-Merchant-Id': self.merch_id,
            'X-Timestamp': str(int(time())),
            'X-Nonce': nonce,
        }

        x_sign = self._make_signature(headers, params)
        headers['X-Sign'] = x_sign
        headers['Content-Type'] = 'application/x-www-form-urlencoded'

        print(headers)
        url = f"{self.BASE_URL}/{endpoint}"

        read_timeout = READ_TIMEOUT
        connect_timeout = CONNECT_TIMEOUT
        if params:
            if 'timeout' in params:
                read_timeout = params['timeout'] + 10
            if 'connect-timeout' in params:
                connect_timeout = params['connect-timeout'] + 10

        response = session.request(
            method,
            url,
            params=params,
            timeout=(connect_timeout, read_timeout),
            proxies=proxy,
            headers=headers,
            data=data,
        )
        print(response)
        return response.json()

    def get_games(self):
        resource = 'games'
        return self._request(endpoint=resource, params={'uuid': '2'})
