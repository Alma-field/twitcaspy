from os import environ
from unittest import TestCase

import vcr

from twitcaspy.api import API
from twitcaspy.auth import AppAuthHandler

from dotenv import load_dotenv
load_dotenv('./.env', encoding='utf-8')
user_id = environ.get('TWITTER_USER_ID', '182224938')
username = environ.get('TWITTER_USERNAME', 'twitcasting_jp')
bearer_token = environ.get('BEARER_TOKEN', '')
client_id = environ.get('CLIENT_ID', '')
client_secret = environ.get('CLIENT_SECRET', '')
use_replay = environ.get('USE_REPLAY', True)

tape = vcr.VCR(
    cassette_library_dir='cassettes',
    filter_headers=['Authorization'],
    serializer='json',
    # Either use existing cassettes, or never use recordings:
    record_mode='new_episodes'#'none' if use_replay else 'all',
)

class TwitcaspyTestCase(TestCase):
    def setUp(self):
        self.auth = AppAuthHandler(client_id, client_secret)
        self.api = API(self.auth)
