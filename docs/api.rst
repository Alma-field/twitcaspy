.. _api_reference:

.. currentmodule:: twitcaspy

.. include:: parameters.rst

*******************************************************
:class:`twitcaspy.API` --- Twitcasting API v2 Reference
*******************************************************

.. autoclass:: API

.. table::
    :align: center

    +------------------------------------------+---------------------------------------+
    | Twitcasting API v2 Endpoint              | :class:`API` Method                   |
    +==========================================+=======================================+
    | .. centered:: :ref:`User`                                                        |
    +------------------------------------------+---------------------------------------+
    | `GET /users/:user_id`_                   | :meth:`API.get_user_info`             |
    +------------------------------------------+---------------------------------------+
    | `GET /verify_credentials`_               | :meth:`API.verify_credentials`        |
    +------------------------------------------+---------------------------------------+
    | .. centered:: :ref:`Live Thumbnail`                                              |
    +------------------------------------------+---------------------------------------+
    | `GET /users/:user_id/live/thumbnail`_    | :meth:`API.get_live_thumbnail_image`  |
    +------------------------------------------+---------------------------------------+
    | .. centered:: :ref:`Movie`                                                       |
    +------------------------------------------+---------------------------------------+
    | `GET /movies/:movie_id`_                 | :meth:`API.get_movie_info`            |
    +------------------------------------------+---------------------------------------+
    | `GET /users/:user_id/movies`_            | :meth:`API.get_movies_by_user`        |
    +------------------------------------------+---------------------------------------+
    | `GET /users/:user_id/current_live`_      | :meth:`API.get_current_live`          |
    +------------------------------------------+---------------------------------------+

.. _GET /users/:user_id: https://apiv2-doc.twitcasting.tv/#get-user-info
.. _GET /verify_credentials: https://apiv2-doc.twitcasting.tv/#verify-credentials
.. _GET /users/:user_id/live/thumbnail: https://apiv2-doc.twitcasting.tv/#get-live-thumbnail-image
.. _GET /movies/:movie_id: https://apiv2-doc.twitcasting.tv/#get-movie-info
.. _GET /users/:user_id/movies: https://apiv2-doc.twitcasting.tv/#get-movies-by-user
.. _GET /users/:user_id/current_live: https://apiv2-doc.twitcasting.tv/#get-current-live

User
====

.. automethod:: API.get_user_info

.. automethod:: API.verify_credentials

Live Thumbnail
==============

.. automethod:: API.get_live_thumbnail_image

Movie
=====

.. automethod:: API.get_movie_info

.. automethod:: API.get_movies_by_user

.. automethod:: API.get_current_live
