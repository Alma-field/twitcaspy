# twitcaspy
[![license](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/Alma-field/twitcaspy/blob/master/LICENSE)
[![test](https://github.com/Alma-field/twitcaspy/actions/workflows/test.yml/badge.svg?branch=master)](https://github.com/Alma-field/twitcaspy/actions/workflows/test.yml)
[![Deploy](https://github.com/Alma-field/twitcaspy/actions/workflows/deploy.yml/badge.svg)](https://github.com/Alma-field/twitcaspy/actions/workflows/deploy.yml)
[![Documentation Status](https://readthedocs.org/projects/twitcaspy/badge/?version=latest)](http://twitcaspy.alma-field.com/en/latest/?badge=latest)
[![GitHub issues open](https://img.shields.io/github/issues/Alma-field/twitcaspy.svg)](https://github.com/Alma-field/twitcaspy/issues?q=is%3Aopen+is%3Aissue)
[![GitHub issues close](https://img.shields.io/github/issues-closed-raw/Alma-field/twitcaspy.svg)](https://github.com/Alma-field/twitcaspy/issues?q=is%3Aclose+is%3Aissue)
[![PyPI Version](https://img.shields.io/pypi/v/twitcaspy?label=PyPI)](https://pypi.org/project/twitcaspy/)
[![Python Versions](https://img.shields.io/pypi/pyversions/twitcaspy?label=Python)](https://pypi.org/project/twitcaspy/)

Twitcatting for Python
Python 3.7 - 3.9 are supported.

## Other language version
 - [English](https://github.com/Alma-field/twitcaspy/blob/master/README.md)
 - [Japanese](https://github.com/Alma-field/twitcaspy/blob/master/README_JA.md)

## Document
 - [develop version](https://twitcaspy.alma-field.com/en/latest)
 - [latest version(v1.1.0)](https://twitcaspy.alma-field.com/en/stable)
 - [v1.1.0](https://twitcaspy.alma-field.com/en/1.1.0)
 - [v1.0.2](https://twitcaspy.alma-field.com/en/1.0.2)
 - [v1.0.1](https://twitcaspy.alma-field.com/en/1.0.1)
 - [v1.0.0](https://twitcaspy.alma-field.com/en/1.0.0)

## Installation
The easiest way to install the latest version from PyPI is by using pip:
```
pip install twitcaspy
```

You can also use Git to clone the repository from GitHub to install the latest
development version:
```
git clone https://github.com/Alma-field/twitcaspy.git
cd twitcaspy
pip install .
```

Alternatively, install directly from the GitHub repository:
```
pip install git+https://github.com/Alma-field/twitcaspy.git
```

## Examples
This is an execution example in the application scope.  
Get the account name of ***@twitcasting_jp***.
```python
from twitcaspy import API, AppAuthHandler
auth = AppAuthHandler(client_id, client_secret)
api = API(auth)

print(api.get_user_info(id='twitcasting_jp').user.name)
# > ?????????????????????
```

See in [examples](https://github.com/Alma-field/twitcaspy/tree/master/examples) for other examples and the entire code.
### Included example
 - [Authorization](https://github.com/Alma-field/twitcaspy/tree/master/examples/auth)
   - [AppAuthHandler](https://github.com/Alma-field/twitcaspy/tree/master/examples/auth/app.py)
   - [GrantAuthHandler](https://github.com/Alma-field/twitcaspy/tree/master/examples/auth/grant.py)
   - [ImplicitAuthHandler](https://github.com/Alma-field/twitcaspy/tree/master/examples/auth/implicit.py)
 - [Realtime API](https://github.com/Alma-field/twitcaspy/blob/master/examples/realtime)
 - [Webhook](https://github.com/Alma-field/twitcaspy/blob/master/examples/webhook)
   - [Server](https://github.com/Alma-field/twitcaspy/blob/master/examples/webhook/server.py)
   - [Client](https://github.com/Alma-field/twitcaspy/blob/master/examples/webhook/client.py)

## Source
This library is based on:
 - [tweepy/tweepy](https://github.com/tweepy/tweepy) - Twitter for Python!
 - [tamago324/PyTwitcasting](https://github.com/tamago324/PyTwitcasting) - PyTwitcasting is a library for API v2 (??) of Twitcasting.

## Links
 - [Twitcasting API Documentation](https://apiv2-doc.twitcasting.tv/)
 - [API ChangeLog](https://github.com/twitcasting/PublicApiV2/blob/master/CHANGELOG.md)
