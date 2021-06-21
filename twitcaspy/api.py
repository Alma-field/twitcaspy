import functools
import logging
import json
from platform import python_version
import sys

import requests

from . import __version__ as twitcaspy_version
from .errors import (
    BadRequest, Forbidden, HTTPException, NotFound, TooManyRequests,
    TwitcaspyException, TwitcastingServerError, Unauthorized
)
from .parsers import Parser, ModelParser, RawParser

log = logging.getLogger(__name__)

def payload(*payload_list, **payload_kwargs):
    if payload_kwargs is None:
        payload_kwargs = {}
    if isinstance(payload_list, tuple):
        for _key in payload_list:
            payload_kwargs[_key] = [_key, False]
    def decorator(method):
        @functools.wraps(method)
        def wrapper(*args, **kwargs):
            kwargs['payload_type'] = payload_kwargs
            return method(*args, **kwargs)
        wrapper.payload_type = payload_kwargs
        return wrapper
    return decorator

class API:
    """Twitcasting API v2.0 Interface

    Parameters
    ----------
    auth: :class:`~twitcaspy.auth.auth.AuthHandler`
        The authentication handler to be used
    host: :class:`str`
        The general REST API host server URL
    parser: :class:`~twitcaspy.parsers.parser.Parser`
        | The Parser instance to use for parsing the response from Twitcasting.
        | defaults to an instance of ModelParser
    user_agent: :class:`str`
        The UserAgent to be used

    Raises
    ------
    TypeError
        If the given parser is not a Parser instance

    References
    ----------
    https://apiv2-doc.twitcasting.tv/
    """

    def __init__(
        self, auth=None, *, host='apiv2.twitcasting.tv',
        parser=None, user_agent=None
    ):
        self.auth = auth
        self.host = host

        if parser is None:
            parser = ModelParser()
        self.parser = parser

        if user_agent is None:
            user_agent = (
                f"Python/{python_version()} "
                f"Requests/{requests.__version__} "
                f"twitcaspy/{twitcaspy_version}"
            )
        self.user_agent = user_agent

        if not isinstance(self.parser, Parser):
            raise TypeError(
                "parser should be an instance of Parser, not " +
                str(type(self.parser))
            )

        self.session = requests.Session()

    def request(
        self, method, endpoint, *, endpoint_parameters=(), params=None,
        headers=None, json_payload=None, parser=None, payload_type=None,
        post_data=None, require_auth=True, **kwargs
    ):
        # If authentication is required and no credentials
        # are provided, throw an error.
        if require_auth and not self.auth:
            raise TwitcaspyException('Authentication required!')

        if headers is None:
            headers = {}
        headers["X-Api-Version"] = '2.0'
        headers["User-Agent"] = self.user_agent

        # Build the request URL
        url = 'https://' + self.host + endpoint

        if params is None:
            params = {}
        for k, arg in kwargs.items():
            if arg is None:
                continue
            if k not in endpoint_parameters:
                log.warning(f'Unexpected parameter: {k}')
            params[k] = str(arg)
        log.debug("PARAMS: %r", params)

        if parser is None:
            parser = self.parser

        try:
            # Execute request
            try:
                response = self.session.request(
                    method, url, params=params, headers=headers,
                    data=json.dumps(post_data), json=json_payload,
                    auth=self.auth.auth
                )
            except Exception as e:
                raise TwitcaspyException(f'Failed to send request: {e}').with_traceback(sys.exc_info()[2])

            # If an error was returned, throw an exception
            self.last_response = response
            if response.status_code == 400:
                raise BadRequest(response)
            if response.status_code == 401:
                raise Unauthorized(response)
            if response.status_code == 403:
                raise Forbidden(response)
            if response.status_code == 404:
                raise NotFound(response)
            if response.status_code == 429:
                raise TooManyRequests(response)
            if response.status_code >= 500:
                raise TwitcastingServerError(response)
            if response.status_code and not 200 <= response.status_code < 300:
                raise HTTPException(response)

            result = parser.parse(
                response, api=self, payload_type=payload_type)

            return result
        finally:
            self.session.close()

    @payload(
        'user', supporter_count=['raw', False],
        supporting_count=['raw', False])
    def get_user_info(self, *, id=None, screen_id=None, **kwargs):
        """get_user_info(*, id=None, screen_id=None)

        | Returns information about the specified user.
        | |id_screenid|

        Parameters
        ----------
        id: :class:`str`
            |id|
            |id_notice|
        screen_id: :class:`str`
            |screen_id|

        Returns
        -------
        :class:`~twitcaspy.models.Result`
            | |attribute|
            | |latelimit|
            | **user** : :class:`~twitcaspy.models.User`
            | **supporter_count** : :class:`~twitcaspy.models.Raw` (:class:`int`)
                Number of user supporters.
            | **supporting_count** : :class:`~twitcaspy.models.Raw` (:class:`int`)
                Number supported user by the user.

        Raises
        ------
        TwitcaspyException
            If both id and screen_id are not specified

        References
        ----------
        https://apiv2-doc.twitcasting.tv/#get-user-info
        """
        target_id = id if id is not None else screen_id
        if target_id is None:
            raise TwitcaspyException(
                'Either an id or screen_id is required for this method.')
        return self.request('GET', f'/users/{target_id}', **kwargs)

    @payload(
        'app', 'user', supporter_count=['raw', False],
        supporting_count=['raw', False])
    def verify_credentials(self, **kwargs):
        """verify_credentials()

        Returns application and user information about the access_token.

        Returns
        -------
        :class:`~twitcaspy.models.Result`
            | |attribute|
            | |latelimit|
            | **app** : :class:`~twitcaspy.models.App`
            | **user** : :class:`~twitcaspy.models.User`
            | **supporter_count** : :class:`~twitcaspy.models.Raw` (:class:`int`)
            | **supporting_count** : :class:`~twitcaspy.models.Raw` (:class:`int`)

        References
        ----------
        https://apiv2-doc.twitcasting.tv/#verify-credentials
        """
        return self.request('GET', '/verify_credentials', **kwargs)

    def get_live_thumbnail_image(self, *, id=None, screen_id=None, **kwargs):
        """get_live_thumbnail_image(*, id=None, screen_id=None,\
                size='small', position='latest')

        | Returns live thumbnail the specified user.
        | Returns an offline image if the user is not streaming now.
        | |id_screenid|

        Parameters
        ----------
        id: :class:`str`
            |id|
            |id_notice|
        screen_id: :class:`str`
            |screen_id|
        size(optional): :class:`str`
            | image size
            | 'large' or 'small' can be specified.(default is 'small'.)
        position(optional): :class:`str`
            | 'beginning' or 'latest' can be specified.(default is 'latest'.)

        Returns
        -------
        :class:`requests.models.Response`
            | Image data is stored in the content attribute.

        Raises
        ------
        TwitcaspyException
            If both id and screen_id are not specified

        References
        ----------
        https://apiv2-doc.twitcasting.tv/#get-live-thumbnail-image
        """
        target_id = id if id is not None else screen_id
        if target_id is None:
            raise TwitcaspyException(
                'Either an id or screen_id is required for this method.')
        return self.request(
            'GET', f'/users/{target_id}/live/thumbnail',
            parser=RawParser, require_auth=False,
            endpoint_parameters=('size', 'position'), **kwargs)

    @payload('movie', broadcaster=['user', False], tags=['raw', False])
    def get_movie_info(self, movie_id, **kwargs):
        """get_movie_info(movie_id)

        Returns information about the specified movie.

        Parameters
        ----------
        movie_id: :class:`str`
            |movie_id|

        Returns
        -------
        :class:`~twitcaspy.models.Result`
            | |attribute|
            | |latelimit|
            | **movie** : :class:`~twitcaspy.models.Movie`
            | **broadcaster** : :class:`~twitcaspy.models.User`
            | **tags** : :class:`~twitcaspy.models.Raw` (:class:`list`)

        References
        ----------
        https://apiv2-doc.twitcasting.tv/#get-movie-info
        """
        return self.request('GET', f'/movies/{movie_id}', **kwargs)

    @payload(movies=['movie', True], total_count=['raw', False])
    def get_movies_by_user(self, *, id=None, screen_id=None, **kwargs):
        """get_movies_by_user(*, id=None, screen_id=None,\
                offset=0, limit=20, slice_id=None)

        | Returns movies of the specified user
          in descending order of creation date and time.
        | |id_screenid|

        Parameters
        ----------
        id: :class:`str`
            |id|
            |id_notice|
        screen_id: :class:`str`
            |screen_id|
        offset(optional): :class:`int`
            | Position from the beginning
            | It can be specified in the range of 0 to 1000.(default is 0.)
        limit(optional): :class:`int`
            | Maximum number of acquisitions
            | It can be specified in the range of 1 to 50.(default is 20.)
            | (In some cases,
              it may return less than the specified number of videos.)
        slice_id(optional): :class:`int` or :class:`None`
            | Gets the movie before this slice_id.
            | It can be specified in the range of 1 or more.
            | (Not specified by default.[= :class:`None`])
            | If you specify this parameter, offset is ignored.

        Returns
        -------
        :class:`~twitcaspy.models.Result`
            | |attribute|
            | |latelimit|
            | **total_count** : :class:`~twitcaspy.models.Raw` (:class:`int`)
            | **movies** : :class:`List` of :class:`~twitcaspy.models.Movie`

        Raises
        ------
        TwitcaspyException
            If both id and screen_id are not specified

        References
        ----------
        https://apiv2-doc.twitcasting.tv/#get-movies-by-user
        """
        target_id = id if id is not None else screen_id
        if target_id is None:
            raise TwitcaspyException(
                'Either an id or screen_id is required for this method.')
        return self.request(
            'GET', f'/users/{target_id}/movies',
            endpoint_parameters=('offset', 'limit', 'slice_id'), **kwargs)

    @payload('movie', broadcaster=['user', False], tags=['raw', False])
    def get_current_live(self, *, id=None, screen_id=None, **kwargs):
        """get_current_live(*, id=None, screen_id=None)

        | Returns live information if the user is streaming now.
        | |id_screenid|

        Parameters
        ----------
        id: :class:`str`
            |id|
            |id_notice|
        screen_id: :class:`str`
            |screen_id|

        Returns
        -------
        :class:`~twitcaspy.models.Result`
            | |attribute|
            | |latelimit|
            | **movie** : :class:`~twitcaspy.models.Movie`
            | **broadcaster** : :class:`~twitcaspy.models.User`
            | **tags** : :class:`~twitcaspy.models.Raw` (:class:`list`)

        Raises
        ------
        TwitcaspyException
            If both id and screen_id are not specified

        References
        ----------
        https://apiv2-doc.twitcasting.tv/#get-current-live
        """
        target_id = id if id is not None else screen_id
        if target_id is None:
            raise TwitcaspyException(
                'Either an id or screen_id is required for this method.')
        return self.request(
            'GET', f'/users/{target_id}/current_live', **kwargs)

    @payload(movie_id=['raw', False], subtitle=['raw', False])
    def set_current_live_subtitle(self, subtitle, *, cut_out=False, **kwargs):
        """set_current_live_subtitle(subtitle, *, cut_out=False)

        | If the user is broadcasting, set a live telop.

        Parameters
        ----------
        subtitle: :class:`str`
            | live telop
        cut_out: :class:`bool`
            | If the subtitle is more than 17 characters, cut out

        Returns
        -------
        :class:`~twitcaspy.models.Result`
            | |attribute|
            | |latelimit|
            | **movie_id** : :class:`~twitcaspy.models.Raw` (:class:`str`)
              |movie_id|
            | **subtitle** : :class:`~twitcaspy.models.Raw` (:class:`str`)

        Raises
        ------
        TwitcaspyException:
            When the subtitle is less than one character.
            When the subtitle is more than 17 characters and cut_out is False.

        References
        ----------
        https://apiv2-doc.twitcasting.tv/#set-current-live-subtitle
        """
        if len(subtitle) < 1:
            raise TwitcaspyException(
                '`subtitle` must be at least one character.')
        if not cut_out and 17 < len(subtitle):
            raise TwitcaspyException(
                'The subtitle must be 17 characters or less.')
        else:
            post_data = {}
            post_data['subtitle'] = subtitle[:17]
        return self.request(
            'POST', '/movies/subtitle', post_data=post_data, **kwargs)

    @payload(movie_id=['raw', False], subtitle=['raw', False])
    def unset_current_live_subtitle(self, **kwargs):
        """unset_current_live_subtitle()

        | If the user is broadcasting, unset a live telop.

        Returns
        -------
        :class:`~twitcaspy.models.Result`
            | |attribute|
            | |latelimit|
            | **movie_id** : :class:`~twitcaspy.models.Raw` (:class:`str`)
              |movie_id|
            | **subtitle** : :class:`~twitcaspy.models.Raw` (:class:`None`)

        References
        ----------
        https://apiv2-doc.twitcasting.tv/#unset-current-live-subtitle
        """
        return self.request('DELETE', '/movies/subtitle', **kwargs)

    @payload(movie_id=['raw', False], hashtag=['raw', False])
    def set_current_live_hashtag(self, hashtag, *, cut_out=False, **kwargs):
        """set_current_live_hashtag(hashtag, *, cut_out=False)

        | If the user is broadcasting, set a live hashtag.

        Parameters
        ----------
        hashtag: :class:`str`
            live hashtag
        cut_out: :class:`bool`
            | If the hashtag is more than 26 characters, cut out

        Returns
        -------
        :class:`~twitcaspy.models.Result`
            | |attribute|
            | |latelimit|
            | **movie_id** : :class:`~twitcaspy.models.Raw` (:class:`str`)
              |movie_id|
            | **hashtag** : :class:`~twitcaspy.models.Raw` (:class:`str`)

        Raises
        ------
        TwitcaspyException:
            When the hashtag is less than one character./
            When the hashtag is more than 26 characters and cut_out is False.

        References
        ----------
        https://apiv2-doc.twitcasting.tv/#set-current-live-hashtag
        """
        if len(hashtag) < 1:
            raise TwitcaspyException(
                '`hashtag` must be at least one character.')
        if not cut_out and 26 < len(hashtag):
            raise TwitcaspyException(
                '`hashtag` must be 26 characters or less.')
        else:
            post_data = {}
            post_data['hashtag'] = hashtag[:26]
        return self.request(
            'POST', '/movies/hashtag', post_data=post_data, **kwargs)

    @payload(movie_id=['raw', False], hashtag=['raw', False])
    def unset_current_live_hashtag(self, **kwargs):
        """unset_current_live_hashtag()

        | If the user is broadcasting, unset a live hashtag.

        Returns
        -------
        :class:`~twitcaspy.models.Result`
            | |attribute|
            | |latelimit|
            | **movie_id** : :class:`~twitcaspy.models.Raw` (:class:`str`)
              |movie_id|
            | **hashtag** : :class:`~twitcaspy.models.Raw` (:class:`None`)

        References
        ----------
        https://apiv2-doc.twitcasting.tv/#unset-current-live-hashtag
        """
        return self.request('DELETE', '/movies/hashtag', **kwargs)

    @payload(
        movie_id=['raw', False],
        all_count=['raw', False],
        comments=['comment', True])
    def get_comments(self, movie_id, **kwargs):
        """get_comments(movie_id, *, offset=0, limit=20, slice_id=None)

        | Returns comments of the specified movie
          in descending order of creation date and time.

        Parameters
        ----------
        movie_id: :class:`str`
            |movie_id|
        offset(optional): :class:`int`
            | Position from the beginning
            | It can be specified in the range of 0 or more.(default is 0.)
        limit(optional): :class:`int`
            | Maximum number of acquisitions
            | It can be specified in the range of 1 to 50.(default is 10.)
            | (In some cases,
              it may return less than the specified number of videos.)
        slice_id(optional): :class:`int` or :class:`None`
            | Gets the comment after this slice_id.
            | It can be specified in the range of 1 or more.
            | (Not specified by default.[= :class:`None`])
            | If you specify this parameter, offset is ignored.
            | `2018-08-28 update <https://github.com/twitcasting/PublicApiV2/blob/master/CHANGELOG.md#2018-08-28>`_
            | The minimum value that can be specified for slice_id is now 1.

        Returns
        -------
        :class:`~twitcaspy.models.Result`
            | |attribute|
            | |latelimit|
            | **movie_id** : :class:`~twitcaspy.models.Raw` (:class:`str`)
              |movie_id|
            | **all_count** : :class:`~twitcaspy.models.Raw` (:class:`int`)
              Total number of comments
            | **comments** : :class:`List` of :class:`~twitcaspy.models.Comment`

        References
        ----------
        https://apiv2-doc.twitcasting.tv/#get-comments
        """
        return self.request(
            'GET', f'/movies/{movie_id}/comments',
            endpoint_parameters=('offset', 'limit', 'slice_id'), **kwargs)

    @payload('comment', movie_id=['raw', False], all_count=['raw', False])
    def post_comment(self, comment, **kwargs):
        """post_comment(comment, *, sns='none')

        | Post a comment.
        | It can be executed only on a user-by-user basis.

        Parameters
        ----------
        comment: :class:`str`
            | Comment text to post.
            | Must be 1 to 140 characters.
        sns: :class:`str`
            | Simultaneous posting to SNS.
            | (Valid only when the user is linked with Twitter or Facebook.)
            | 'reply' : Post in a format that replies to the streamer.
            | 'normal' : Regular post.
            | 'none' : No SNS posts.

        Returns
        -------
        :class:`~twitcaspy.models.Result`
            | |attribute|
            | |latelimit|
            | **movie_id** : :class:`~twitcaspy.models.Raw` (:class:`str`)
              |movie_id|
            | **all_count** : :class:`~twitcaspy.models.Raw` (:class:`int`)
              Total number of comments
            | **comment** : :class:`~twitcaspy.models.Comment`

        Raises
        ------
        TwitcaspyException:
            When comment is not 1-140 characters.

        References
        ----------
        https://apiv2-doc.twitcasting.tv/#post-comment
        """
        if not 1 <= len(hashtag) <= 140:
            raise TwitcaspyException(
                '`comment` must be in the range 1-140 characters.')
        else:
            post_data = {'comment': comment}
        return self.request(
            'POST', f'/movies/{movie_id}/comments',
            post_data=post_data, **kwargs)

    @payload(comment_id=['raw', False])
    def delete_comment(self, movie_id, comment_id, **kwargs):
        """delete_comment(movie_id, comment_id)

        | Delete the comment.
        | It can be executed only on a user-by-user basis.
        | As a general rule, the comments that can be deleted are limited to
          those that the poster is the same as the user associated
          with the access token.
        | However, if you use the access token of the user who owns the movie,
          you can delete the comments posted by other users.

        Parameters
        ----------
        movie_id: :class:`str`
            |movie_id|
        comment_id: :class:`str`
            |comment_id|

        Returns
        -------
        :class:`~twitcaspy.models.Result`
            | |attribute|
            | |latelimit|
            | **comment_id** : :class:`~twitcaspy.models.Raw` (:class:`str`)
              ID of the deleted comment.

        References
        ----------
        https://apiv2-doc.twitcasting.tv/#delete-comment
        """
        return self.request('DELETE', f'/movies/{movie_id}/comments/{comment_id}', **kwargs)

    @payload(slice_id=['raw', False], gifts=['gift', True])
    def get_gifts(self, **kwargs):
        """get_gifts(*, slice_id=-1)

        | Acquire the item sent by the user associated
          with the access token in the last 10 seconds.

        Parameters
        ----------
        slice_id(optional): :class:`int`
            | Gets the items sent after this item send ID.
            | It can be specified in the range of -1 or more.(default is -1.)

        Returns
        -------
        :class:`~twitcaspy.models.Result`
            | |attribute|
            | |latelimit|
            | **slice_id** : :class:`~twitcaspy.models.Raw` (:class:`int`)
              Slice_id to be specified the next time you call the API.
            | **gifts** : :class:`list` of :class:`~twitcaspy.models.Gift`

        References
        ----------
        https://apiv2-doc.twitcasting.tv/#get-gifts
        """
        return self.request(
            'GET', '/gifts',
            endpoint_parameters=('slice_id'), **kwargs)

    @payload(is_supporting=['raw', False], target_user=['user', False])
    def get_supporting_status(self, *, id=None, screen_id=None, **kwargs):
        """get_supporting_status(*, id=None, screen_id=None)

        | Gets the status of whether a user is a supporter of another user.
        | |id_screenid|

        Parameters
        ----------
        id: :class:`str`
            |id|
            |id_notice|
        screen_id: :class:`str`
            |screen_id|

        Returns
        -------
        :class:`~twitcaspy.models.Result`
            | |attribute|
            | |latelimit|
            | **is_supporting** : :class:`~twitcaspy.models.Raw` (:class:`bool`)
              Whether it is a supporter.
            | **target_user** : :class:`~twitcaspy.models.User`
              Target user information

        Raises
        ------
        TwitcaspyException
            If both id and screen_id are not specified

        References
        ----------
        https://apiv2-doc.twitcasting.tv/#get-supporting-status
        """
        target_id = id if id is not None else screen_id
        if target_id is None:
            raise TwitcaspyException(
                'Either an id or screen_id is required for this method.')
        return self.request(
            'GET', f'/users/{target_id}/supporting_status', **kwargs)

    @payload(added_count=['raw', False])
    def support_user(self, target_user_ids=None, **kwargs):
        """support_user(target_user_ids=None)

        | Become a supporter of the specified user.

        Parameters
        ----------
        target_user_ids: :class:`list` or :class:`tuple`
            | An array of target user id or screen_id
            | The number of elements in the array must be 20 or less.

        Returns
        -------
        :class:`~twitcaspy.models.Result`
            | |attribute|
            | |latelimit|
            | **added_count** : :class:`~twitcaspy.models.Raw` (:class:`int`)
              Number of registered supporters.

        Raises
        ------
        TwitcaspyException
            When target_user_ids is not a :class:`list` or :class:`tuple`

        References
        ----------
        https://apiv2-doc.twitcasting.tv/#support-user
        """
        if not isinstance(target_user_ids, (list, tuple)):
            raise TwitcaspyException("target_user_ids must be list or tuple, not "
                            + type(target_user_ids).__name__)
        post_data = {'target_user_ids': target_user_ids}
        return self.request(
            'PUT', '/support', post_data=post_data, **kwargs)
