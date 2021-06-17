import functools
import logging
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
    auth
        The authentication handler to be used
    host
        The general REST API host server URL
    parser
        The Parser instance to use for parsing the response from Twitcasting;
        defaults to an instance of ModelParser

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
                    data=post_data, json=json_payload, auth=self.auth.auth
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
        """
        Returns information about the specified user.

        Parameters
        ----------
        Either an id or screen_id is required for this method.
        If both are specified, the id takes precedence.
        id
            |id|
        screen_id
            |screen_id|

        Returns
        -------
        :class:`~twitcaspy.models.Result`
                 |- user: twitcaspy.models.User
                 |- supporter_count: twitcaspy.models.Raw(int)
                 |- supporting_count: twitcaspy.models.Raw(int)

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
        """
        Returns application and user information about the access_token.

        Returns
        -------
        :class:`~twitcaspy.models.Result`
                 |- app: twitcaspy.models.App
                 |- user: twitcaspy.models.User
                 |- supporter_count: twitcaspy.models.Raw(int)
                 |- supporting_count: twitcaspy.models.Raw(int)

        References
        ----------
        https://apiv2-doc.twitcasting.tv/#verify-credentials
        """
        return self.request('GET', '/verify_credentials', **kwargs)

    def get_live_thumbnail_image(self, *, id=None, screen_id=None, **kwargs):
        """get_live_thumbnail_image(self, *, id=None, screen_id=None,
                size='small', position='latest')

        Returns live thumbnail the specified user.
        Returns an offline image if the user is not streaming now.

        Parameters
        ----------
        Either an id or screen_id is required for this method.
        If both are specified, the id takes precedence.
        id
            |id|
        screen_id
            |screen_id|
        size
            |size|: image size(optional)
            'large' or 'small' can be specified.(default is 'small'.)
        position
            |position|: (optional)
            'beginning' or 'latest' can be specified.(default is 'latest'.)

        Returns
        -------
        :class:`requests.models.Response`

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
            parser=RawParser, **kwargs)

    @payload('movie', broadcaster=['user', False], tags=['raw', False])
    def get_movie_info(self, *, movie_id, **kwargs):
        """
        Returns information about the specified user.

        Parameters
        ----------
        movie_id
            |movie_id|

        Returns
        -------
        :class:`~twitcaspy.models.Result`
                 |- movie: twitcaspy.models.Movie
                 |- broadcaster: twitcaspy.models.User
                 |- tags: twitcaspy.models.Raw(list)

        References
        ----------
        https://apiv2-doc.twitcasting.tv/#get-movie-info
        """
        return self.request('GET', f'/movies/{movie_id}', **kwargs)
