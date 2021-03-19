import base64
import random
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


class CasinoClass:
    BASE_URL = 'https://game-aggregator.com/api/v1/'

    def __init__(self, merch_id, merch_key):
        self.merch_id = merch_id
        self.merch_key = merch_key
        # self.nonce = nonce

    def _make_signature(self, headers, params):
        sorted_dict = dict(sorted({**headers, **params}.items()))
        string_from_dict = urlencode(sorted_dict)
        hashed = hmac.new(b'self.merch_key', string_from_dict.encode(), sha1)
        print(hashed)
        return base64.encodebytes(hashed.digest()).decode('utf-8')

    def _request(self, endpoint, method='get', params=None, data=None, proxy=None):

        t = time()
        nonce = ''.join([str(random.randint(0, 9)) for _ in range(8)])

        headers = {
            'X-Merchant-Id': self.merch_id,
            'X-Timestamp': str(int(t)),
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

        return response.json()

    def get_games(self):
        resource = 'games'
        return self._request(endpoint=resource, params={"qwe": "qwe"})
