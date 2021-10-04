# Twitcaspy
# Copyright 2021 Alma-field
# See LICENSE for details.

# Before running this code, run the following command:
# このコードを実行する前に、以下のコマンドを実行してください。
# pip install twitcaspy[webhook]

from flask import Flask, request, make_response, jsonify, abort
app = Flask(__name__)

from twitcaspy import api, TwitcaspyException

@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        webhook = api.incoming_webhook(request.json)
        #Show Parse Result
        print(f'signature : {webhook.signature}')
        print(f'user_id : {webhook.broadcaster.id}')
        print(f'title : {webhook.movie.title}')
    return make_response(jsonify({'message':'OK'}))

if __name__ == '__main__':
    import json
    cassettes_file = '../../cassettes/testincomingwebhook.json'
    # load test webhook data
    with open(cassettes_file, "r", encoding='utf-8')as file:
        data = json.load(file)
        # set signature to api instance
        api.signature = data['signature']
    app.run(debug=True)
