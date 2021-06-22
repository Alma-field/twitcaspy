# Twitcaspy
# Copyright 2021 Alma-field
# See LICENSE for details.

from .app import App

from .comment import Comment

from .gift import Gift

from .movie import Movie

from .raw import Raw

from .subcategory import SubCategory

from .supporter import Supporter

from .user import User

class ModelFactory:
    """
    | Used by parsers for creating instances of models.
    | You may subclass this factory to add your own extended models.
    """

    app = App
    comment = Comment
    gift = Gift
    movie = Movie
    raw = Raw
    subcategory = SubCategory
    supporter = Supporter
    user = User
