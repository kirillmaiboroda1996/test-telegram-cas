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
from collections import OrderedDict

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
        string_from_dict = urlencode(sorted_dict).encode('utf-8')
        print(string_from_dict)
        hashed = hmac.new(self.merch_key.encode('utf-8'), string_from_dict, sha1)
        return hashed.hexdigest()

    def _request(self, endpoint, method='get', params=None, data=None, proxy=None):
        nonce = uuid.uuid4().hex
        t = str(int(time()))
        auth_headers = {
            'X-Merchant-Id': self.merch_id,
            'X-Timestamp': t,
            'X-Nonce': nonce,
        }
        print(auth_headers)
        headers = {
            'X-Merchant-Id': self.merch_id,
            'X-Timestamp': t,
            'X-Nonce': nonce,
            'X-Sign': self._make_signature(params, auth_headers),
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        print(headers)
        url = f"{self.BASE_URL}/{endpoint}"
        print(url)
        read_timeout = READ_TIMEOUT
        connect_timeout = CONNECT_TIMEOUT
        if params:
            if 'timeout' in params:
                read_timeout = params['timeout'] + 10
            if 'connect-timeout' in params:
                connect_timeout = params['connect-timeout'] + 10

        response = requests.request(
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
        return self._request(endpoint=resource, params={})
