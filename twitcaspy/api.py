import logging
from platform import python_version
import sys

import requests

from . import __version__ as twitcaspy_version
from .parsers import Parser, ModelParser

log = logging.getLogger(__name__)

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

