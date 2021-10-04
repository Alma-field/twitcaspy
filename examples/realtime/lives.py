# Twitcaspy
# Copyright 2021 Alma-field
# See LICENSE for details.

# Before running this code, run the following command:
# このコードを実行する前に、以下のコマンドを実行してください。
# pip install twitcaspy[realtime]

from base64 import b64encode
# The client id and/or secret can be found on your application's Details page
# located at select app in https://twitcasting.tv/developer.php
# (in "details" tab)
CLIENT_ID = ''
CLIENT_SECRET = ''
# generate basic token
BASIC_TOKEN = b64encode(f'{CLIENT_ID}:{CLIENT_SECRET}'.encode('utf-8')).decode('utf-8')
# create Authorization header
HEADERS = {'Authorization': f'Basic {BASIC_TOKEN}'}
# create socket url
SOCKET_URL = f'wss://{CLIENT_ID}:{CLIENT_SECRET}@realtime.twitcasting.tv/lives'

from twitcaspy.parsers import ModelParser
# set parse keywords
parser_kwargs = {'movies': ['live', True]}
parser = ModelParser()

import json

def on_message(ws, message):
    try:
        # try parse from json text
        data = json.loads(message)
    except:
        print(type(message))
        print(message)
        return
    if 'hello' in data:
        # first message
        print(f'hello: {data["hello"]}')
    else:
        # parse object
        lives = parser.parse(payload=data, payload_type=parser_kwargs)
        flag = True
        for live in lives.movies:
            if flag:
                flag = False
            else:
                print('-'*25)
            # shoe user name and screen name
            print(f' name: {live.broadcaster.name}({live.broadcaster.screen_id})')
            # show live title and subtitle
            print(f'title: {live.movie.title}({live.movie.subtitle})')
    print('-'*50)

if __name__ == "__main__":
    import websocket
    #websocket.enableTrace(True)
    # create websocket instance
    ws = websocket.WebSocketApp(
        SOCKET_URL, header=HEADERS, on_message=on_message)
    # run websocket
    ws.run_forever()
