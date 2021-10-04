# Twitcaspy
# Copyright 2021 Alma-field
# See LICENSE for details.

from twitcaspy import API, AppAuthHandler

# The client id and/or secret can be found on your application's Details page
# located at select app in https://twitcasting.tv/developer.php
# (in "details" tab)
CLIENT_ID = ''
CLIENT_SECRET = ''

auth = AppAuthHandler(CLIENT_ID, CLIENT_SECRET)
api = API(auth)

# Target User ID and screen ID
user_id = '182224938'
screen_id = 'twitcasting_jp'

# If the authentication was successful, you should
# see the name of the account print out
print(api.get_user_info(id=user_id).user.name)

result = api.get_webhook_list()
print(result.all_count)
for webhook in result.webhooks:
    print(f'{webhook.user_id}: {event}')
