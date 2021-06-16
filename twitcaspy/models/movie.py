# Twitcaspy
# Copyright 2021 Alma-field
# See LICENSE for details.

from .model import Model

class Movie(Model):
    """
    Movie Object : https://apiv2-doc.twitcasting.tv/#movie-object
    """

    @classmethod
    def parse(cls, api, json, *, tags=[]):
        movie = cls(api)
        setattr(movie, '_json', json)
        for k, v in json.items():
            if k == 'created':
                setattr(movie, k, fromtimestamp(v))
            else:
                setattr(movie, k, v)
        return movie
