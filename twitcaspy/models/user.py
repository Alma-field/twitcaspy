# Twitcaspy
# Copyright 2021 Alma-field
# See LICENSE for details.

from .model import Model

class User(Model):
    """
    User Object : https://apiv2-doc.twitcasting.tv/#user-object
    """

    @classmethod
    def parse(cls, api, json):
        user = cls(api)
        setattr(user, '_json', json)
        for k, v in json.items():
            setattr(user, k, v)
        return user
