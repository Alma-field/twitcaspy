# Twitcaspy
# Copyright 2021 Alma-field
# See LICENSE for details.

from requests.auth import AuthBase

class OAuth2Bearer(AuthBase):
    """Bearer Authentication

    Parameters
    ----------
    bearer_token: :class:`str`
        |bearer_token|

    Raises
    ------
    TypeError
        If the given bearer_token is not a string instance
    """
    def __init__(self, bearer_token):
        self.bearer_token = bearer_token

    def __call__(self, request):
        request.headers['Authorization'] = 'Bearer ' + self.bearer_token
        return request
