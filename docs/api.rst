.. _api_reference:

.. currentmodule:: twitcaspy

.. include:: parameters.rst

*******************************************************
:class:`twitcaspy.API` --- Twitcasting API v2 Reference
*******************************************************

.. autoclass:: API

.. table::
    :align: center

    +--------------------------------------------------+-----------------------------------------+
    | Twitcasting API v2 Endpoint                      | :class:`API` Method                     |
    +==================================================+=========================================+
    | .. centered:: :ref:`User`                                                                  |
    +--------------------------------------------------+-----------------------------------------+
    | `GET /users/:user_id`_                           | :meth:`API.get_user_info`               |
    +--------------------------------------------------+-----------------------------------------+
    | `GET /verify_credentials`_                       | :meth:`API.verify_credentials`          |
    +--------------------------------------------------+-----------------------------------------+
    | .. centered:: :ref:`Live Thumbnail`                                                        |
    +--------------------------------------------------+-----------------------------------------+
    | `GET /users/:user_id/live/thumbnail`_            | :meth:`API.get_live_thumbnail_image`    |
    +--------------------------------------------------+-----------------------------------------+
    | .. centered:: :ref:`Movie`                                                                 |
    +--------------------------------------------------+-----------------------------------------+
    | `GET /movies/:movie_id`_                         | :meth:`API.get_movie_info`              |
    +--------------------------------------------------+-----------------------------------------+
    | `GET /users/:user_id/movies`_                    | :meth:`API.get_movies_by_user`          |
    +--------------------------------------------------+-----------------------------------------+
    | `GET /users/:user_id/current_live`_              | :meth:`API.get_current_live`            |
    +--------------------------------------------------+-----------------------------------------+
    | `POST /movies/subtitle`_                         | :meth:`API.set_current_live_subtitle`   |
    +--------------------------------------------------+-----------------------------------------+
    | `DELETE /movies/subtitle`_                       | :meth:`API.unset_current_live_subtitle` |
    +--------------------------------------------------+-----------------------------------------+
    | `POST /movies/hashtag`_                          | :meth:`API.set_current_live_hashtag`    |
    +--------------------------------------------------+-----------------------------------------+
    | `DELETE /movies/hashtag`_                        | :meth:`API.unset_current_live_hashtag`  |
    +--------------------------------------------------+-----------------------------------------+
    | .. centered:: :ref:`Comment`                                                               |
    +--------------------------------------------------+-----------------------------------------+
    | `GET /movies/:movie_id/comments`_                | :meth:`API.get_comments`                |
    +--------------------------------------------------+-----------------------------------------+
    | `POST /movies/:movie_id/comments`_               | :meth:`API.post_comments`               |
    +--------------------------------------------------+-----------------------------------------+
    | `DELETE /movies/:movie_id/comments/:comment_id`_ | :meth:`API.delete_comment`              |
    +--------------------------------------------------+-----------------------------------------+
    | .. centered:: :ref:`Gift`                                                                  |
    +--------------------------------------------------+-----------------------------------------+
    | `GET /gifts`_                                    | :meth:`API.get_gifts`                   |
    +--------------------------------------------------+-----------------------------------------+
    | .. centered:: :ref:`Supporter`                                                             |
    +--------------------------------------------------+-----------------------------------------+
    | `GET /users/:user_id/supporting_status`_         | :meth:`API.get_supporting_status`       |
    +--------------------------------------------------+-----------------------------------------+
    | `PUT /support`_                                  | :meth:`API.support_user`                |
    +--------------------------------------------------+-----------------------------------------+
    | `PUT /unsupport`_                                | :meth:`API.unsupport_user`              |
    +--------------------------------------------------+-----------------------------------------+
    | `GET /users/:user_id/supporting`_                | :meth:`API.supporting_list`             |
    +--------------------------------------------------+-----------------------------------------+
    | `GET /users/:user_id/supporters`_                | :meth:`API.supporter_list`              |
    +--------------------------------------------------+-----------------------------------------+
    | `GET /categories`_                               | :meth:`API.get_categories`              |
    +--------------------------------------------------+-----------------------------------------+
    | `GET /search/users`_                             | :meth:`API.search_users`                |
    +--------------------------------------------------+-----------------------------------------+
    | `GET /search/lives`_                             | :meth:`API.search_live_movies`          |
    +--------------------------------------------------+-----------------------------------------+
    |                                                  | :meth:`API.incoming_webhook`            |
    +--------------------------------------------------+-----------------------------------------+
    | `GET /webhooks`_                                 | :meth:`API.get_webhook_list`            |
    +--------------------------------------------------+-----------------------------------------+
    | `POST /webhooks`_                                | :meth:`API.register_webhook`            |
    +--------------------------------------------------+-----------------------------------------+
    | `DELETE /webhooks`_                              | :meth:`API.remove_webhook`              |
    +--------------------------------------------------+-----------------------------------------+
    | `GET /rtmp_url`_                                 | :meth:`API.get_rtmp_url`                |
    +--------------------------------------------------+-----------------------------------------+

.. _GET /users/:user_id: https://apiv2-doc.twitcasting.tv/#get-user-info
.. _GET /verify_credentials: https://apiv2-doc.twitcasting.tv/#verify-credentials
.. _GET /users/:user_id/live/thumbnail: https://apiv2-doc.twitcasting.tv/#get-live-thumbnail-image
.. _GET /movies/:movie_id: https://apiv2-doc.twitcasting.tv/#get-movie-info
.. _GET /users/:user_id/movies: https://apiv2-doc.twitcasting.tv/#get-movies-by-user
.. _GET /users/:user_id/current_live: https://apiv2-doc.twitcasting.tv/#get-current-live
.. _POST /movies/subtitle: https://apiv2-doc.twitcasting.tv/#set-current-live-subtitle
.. _DELETE /movies/subtitle: https://apiv2-doc.twitcasting.tv/#unset-current-live-subtitle
.. _POST /movies/hashtag: https://apiv2-doc.twitcasting.tv/#set-current-live-hashtag
.. _DELETE /movies/hashtag: https://apiv2-doc.twitcasting.tv/#unset-current-live-hashtag
.. _GET /movies/:movie_id/comments: https://apiv2-doc.twitcasting.tv/#get-comments
.. _POST /movies/:movie_id/comments: https://apiv2-doc.twitcasting.tv/#post-comments
.. _DELETE /movies/:movie_id/comments/:comment_id: https://apiv2-doc.twitcasting.tv/#delete-comment
.. _GET /gifts: https://apiv2-doc.twitcasting.tv/#get-gifts
.. _GET /users/:user_id/supporting_status: https://apiv2-doc.twitcasting.tv/#get-supporting-status
.. _PUT /support: https://apiv2-doc.twitcasting.tv/#support-user
.. _PUT /unsupport: https://apiv2-doc.twitcasting.tv/#unsupport-user
.. _GET /users/:user_id/supporting: https://apiv2-doc.twitcasting.tv/#supporting-list
.. _GET /users/:user_id/supporters: https://apiv2-doc.twitcasting.tv/#supporter-list
.. _GET /categories: https://apiv2-doc.twitcasting.tv/#get-categories
.. _GET /search/users: https://apiv2-doc.twitcasting.tv/#search-users
.. _GET /search/lives: https://apiv2-doc.twitcasting.tv/#search-live-movies
.. _GET /webhooks: https://apiv2-doc.twitcasting.tv/#get-webhook-list
.. _POST /webhooks: https://apiv2-doc.twitcasting.tv/#register-webhook
.. _DELETE /webhooks: https://apiv2-doc.twitcasting.tv/#remove-webhook
.. _GET /rtmp_url: https://apiv2-doc.twitcasting.tv/#get-rtmp-url

User
----

get_user_info
=============
.. automethod:: API.get_user_info

verify_credentials
==================
.. automethod:: API.verify_credentials

Live Thumbnail
--------------

get_live_thumbnail_image
========================
.. automethod:: API.get_live_thumbnail_image

Movie
-----

get_movie_info
==============
.. automethod:: API.get_movie_info

get_movies_by_user
==================
.. automethod:: API.get_movies_by_user

get_current_live
================
.. automethod:: API.get_current_live

set_current_live_subtitle
=========================
.. automethod:: API.set_current_live_subtitle

unset_current_live_subtitle
===========================
.. automethod:: API.unset_current_live_subtitle

set_current_live_hashtag
=========================
.. automethod:: API.set_current_live_hashtag

unset_current_live_hashtag
===========================
.. automethod:: API.unset_current_live_hashtag

Comment
-------

get_comments
============
.. automethod:: API.get_comments

post_comment
============
.. automethod:: API.post_comment

delete_comment
==============
.. automethod:: API.delete_comment

Gift
----

get_gifts
=========
.. automethod:: API.get_gifts

Supporter
---------

get_supporting_status
=====================
.. automethod:: API.get_supporting_status

support_user
============
.. automethod:: API.support_user

unsupport_user
==============
.. automethod:: API.unsupport_user

supporting_list
===============
.. automethod:: API.supporting_list

supporter_list
==============
.. automethod:: API.supporter_list

Category
--------

get_categories
==============
.. automethod:: API.get_categories

Search users and movies
-----------------------

search_users
============
.. automethod:: API.search_users

search_live_movies
==================
.. automethod:: API.search_live_movies

WebHook
-------

incoming_webhook
================
.. automethod:: API.incoming_webhook

get_webhook_list
================
.. automethod:: API.get_webhook_list

register_webhook
================
.. automethod:: API.register_webhook

remove_webhook
==============
.. automethod:: API.remove_webhook

Broadcasting
------------

get_rtmp_url
============
.. automethod:: API.get_rtmp_url
