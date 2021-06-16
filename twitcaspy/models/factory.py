# Twitcaspy
# Copyright 2021 Alma-field
# See LICENSE for details.

from .raw import Raw

from .user import User

class ModelFactory:
    """
    Used by parsers for creating instances of models.
    You may subclass this factory to add your own extended models.
    """

    raw = Raw
    user = User
