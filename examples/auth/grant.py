# Twitcaspy
# Copyright 2021 Alma-field
# See LICENSE for details.

from twitcaspy import API, GrantAuthHandler

# The client id and/or secret can be found on your application's Details page
# located at select app in https://twitcasting.tv/developer.php
# (in "details" tab)
CLIENT_ID = ''
CLIENT_SECRET = ''
CALLBACK_URL = ''

auth = GrantAuthHandler(CLIENT_ID, CLIENT_SECRET, CALLBACK_URL)

# Open webbrowser
print(f'URL: {auth.get_authorization_url()}')
webbrowser.open(auth.get_authorization_url())
redirect_uri = input('input redirect_uri > ')
auth.fetch_token(redirect_uri)
api = API(auth)

# Get Verify credentials
credential = api.verify_credentials()
# If you uncomment it, the Response body is displayed.
# (コメントアウトを外すとレスポンス本体が表示されます。)
#print(credential._json)

# If you uncomment it,
# the name of the application you are using will be displayed.
# (コメントアウトを外すと使用しているアプリケーションの名前が表示されます。)
#print(credential.app.name)

# If the authentication was successful,
# you should see the name of the account print out
# (認証に成功している場合、アカウント名が表示されます。)
print(credential.user.name)

# Target User ID and screen ID
user_id = '182224938'
screen_id = 'twitcasting_jp'

user_info = api.get_user_info(id=user_id)
# If the authentication was successful, you should
# see the name of the account print out
# (認証に成功している場合、アカウント名が表示されます。)
print(user_info.user.name)
