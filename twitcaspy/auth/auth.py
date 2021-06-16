# Twitcaspy
# Copyright 2021 Alma-field
# See LICENSE for details.

class AuthHandler:
    OAUTH_HOST = 'apiv2.twitcasting.tv'
    OAUTH_ROOT = '/oauth2/'

    def __init__(self, client_id, client_secret):
        if not isinstance(client_id, str):
            raise TypeError("ClientID must be string, not "
                            + type(client_id).__name__)
        if not isinstance(client_secret, str):
            raise TypeError("Client secret must be string, not "
                            + type(client_secret).__name__)

        self.client_id = client_id
        self.client_secret = client_secret

    def _get_oauth_url(self, endpoint):
        return 'https://' + self.OAUTH_HOST + self.OAUTH_ROOT + endpoint

    def apply_auth(self, url, method, headers, parameters):
        """Apply authentication headers to request"""
        raise NotImplementedError
