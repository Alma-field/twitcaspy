# twitcaspy
[![license](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/Alma-field/twitcaspy/blob/master/LICENSE)
[![test](https://github.com/Alma-field/twitcaspy/actions/workflows/test.yml/badge.svg?branch=master)](https://github.com/Alma-field/twitcaspy/actions/workflows/test.yml)
[![Deploy](https://github.com/Alma-field/twitcaspy/actions/workflows/deploy.yml/badge.svg)](https://github.com/Alma-field/twitcaspy/actions/workflows/deploy.yml)
[![Documentation Status](https://readthedocs.org/projects/twitcaspy/badge/?version=latest)](http://twitcaspy.alma-field.com/ja/latest/?badge=latest)
[![GitHub issues open](https://img.shields.io/github/issues/Alma-field/twitcaspy.svg)](https://github.com/Alma-field/twitcaspy/issues?q=is%3Aopen+is%3Aissue)
[![GitHub issues close](https://img.shields.io/github/issues-closed-raw/Alma-field/twitcaspy.svg)](https://github.com/Alma-field/twitcaspy/issues?q=is%3Aclose+is%3Aissue)
[![PyPI Version](https://img.shields.io/pypi/v/twitcaspy?label=PyPI)](https://pypi.org/project/twitcaspy/)
[![Python Versions](https://img.shields.io/pypi/pyversions/twitcaspy?label=Python)](https://pypi.org/project/twitcaspy/)

Python用Twitcattingクライアントライブラリ
Python 3.7 - 3.9 がサポートされています。

## Other language version/他言語版
 - [English/英語](README.md)
 - [Japanese/日本語](README_JA.md)

## ドキュメント
 - [開発版](https://twitcaspy.alma-field.com/ja/latest)
 - [最新版 (v1.1.0)](https://twitcaspy.alma-field.com/ja/stable)
 - [v1.1.0](https://twitcaspy.alma-field.com/ja/1.1.0)
 - [v1.0.2](https://twitcaspy.alma-field.com/ja/1.0.2)
 - [v1.0.1](https://twitcaspy.alma-field.com/ja/1.0.1)
 - [v1.0.0](https://twitcaspy.alma-field.com/ja/1.0.0)

## インストール
PyPIから最新バージョンはpipを用いてインストールできます。
```
pip install twitcaspy
```

GitHubからリポジトリのクローンを作成することで、最新の開発バージョンをインストールすることもできます。
```
git clone https://github.com/Alma-field/twitcaspy.git
cd twitcaspy
pip install .
```

または、GitHubリポジトリから直接インストールします。
```
pip install git+https://github.com/Alma-field/twitcaspy.git
```

## 例
アプリケーションスコープでの実行例です。    
***@twitcasting_jp*** のアカウント名を取得します。
```python
from twitcaspy import API, AppAuthHandler
auth = AppAuthHandler(client_id, client_secret)
api = API(auth)

print(api.get_user_info(id='twitcasting_jp').user.name)
# > ツイキャス公式
```

その他の例やコード全体は[examples](https://github.com/Alma-field/twitcaspy/tree/master/examples)内のコードをご覧ください。
### 含まれている例
 - [Authorization](https://github.com/Alma-field/twitcaspy/tree/master/examples/auth)
   - [AppAuthHandler](https://github.com/Alma-field/twitcaspy/tree/master/examples/auth/app.py)
   - [GrantAuthHandler](https://github.com/Alma-field/twitcaspy/tree/master/examples/auth/grant.py)
   - [ImplicitAuthHandler](https://github.com/Alma-field/twitcaspy/tree/master/examples/auth/implicit.py)
 - [Realtime API](https://github.com/Alma-field/twitcaspy/blob/master/examples/realtime)
 - [Webhook](https://github.com/Alma-field/twitcaspy/blob/master/examples/webhook)
   - [Server](https://github.com/Alma-field/twitcaspy/blob/master/examples/webhook/server.py)
   - [Client](https://github.com/Alma-field/twitcaspy/blob/master/examples/webhook/client.py)

## 出典
このライブラリは以下を参考にしています:
 - [tweepy/tweepy](https://github.com/tweepy/tweepy) - Twitter for Python!
 - [tamago324/PyTwitcasting](https://github.com/tamago324/PyTwitcasting) - PyTwitcasting is a library for API v2 (β) of Twitcasting.

## リンク
 - [Twitcasting API Documentation](https://apiv2-doc.twitcasting.tv/)
 - [API ChangeLog](https://github.com/twitcasting/PublicApiV2/blob/master/CHANGELOG.md)
