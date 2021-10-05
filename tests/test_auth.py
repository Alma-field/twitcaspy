# Twitcaspy
# Copyright 2021 Alma-field
# See LICENSE for details.
#
# based on tweepy(https://github.com/tweepy/tweepy)
# Copyright (c) 2009-2021 Joshua Roesslein

from unittest import TestCase
from nose.tools import ok_

from .config import *
from twitcaspy import API, GrantAuthHandler

class TwitcaspyAuthTests(TestCase):

    def testoauth(self):
        if not client_id or not client_secret:
            self.skipTest("Missing client id and/or secret")

        auth = GrantAuthHandler(client_id, client_secret)

        # test getting access token
        auth_url = auth.get_authorization_url()
        print('Please authorize: ' + auth_url)
        authorization_response = input('Enter the full callback URL\n')
        auth.fetch_token(authorization_response)
        ok_(auth.oauth.token['access_token'] is not None)

        # build api object test using oauth
        api = API(auth)
        result = api.verify_credentials()
