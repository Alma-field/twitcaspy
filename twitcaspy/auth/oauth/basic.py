# Twitcaspy
# Copyright 2021 Alma-field
# See LICENSE for details.

from base64 import b64encode

from requests.auth import AuthBase

class OAuth2Basic(AuthBase):
    def __init__(self, client_id, client_secret):
        self.token = b64encode(f'{client_id}:{client_secret}'.encode('utf-8'))
        self.token = self.token.decode('utf-8')

    def __call__(self, request):
        request.headers['Authorization'] = 'Basic ' + self.token
        return request
