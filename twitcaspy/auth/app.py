# Twitcaspy
# Copyright 2021 Alma-field
# See LICENSE for details.

from .auth import AuthHandler

from .oauth import OAuth2Basic

class AppAuthHandler(AuthHandler):
    """
    Application-only authentication handler

    Parameters
    ----------
    client_id
        client_id of this app
    client_secret
        client_secret of this app

    References
    ----------
    https://apiv2-doc.twitcasting.tv/#access-token
    """

    def __init__(self, client_id, client_secret):
        super().__init__(client_id, client_secret)
        self.auth = OAuth2Basic(client_id, client_secret)