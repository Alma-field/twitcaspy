# Twitcaspy
# Copyright 2021 Alma-field
# See LICENSE for details.

from flask import Flask, request, make_response, jsonify, abort
app = Flask(__name__)

from twitcaspy import api, TwitcaspyException

@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        try:
            webhook = api.incoming_webhook(request.json)
            #Show Parse Result
            print(f'signature : {webhook.signature}')
            print(f'user_id : {webhook.broadcaster.id}')
            print(f'title : {webhook.movie.title}')
        except TwitcaspyException:
            abort(404)
    return make_response(jsonify({'message':'OK'}))

if __name__ == '__main__':
    import json
    cassettes_file = '../../cassettes/testincomingwebhook.json'
    with open(cassettes_file, "r", encoding='utf-8')as file:
        data = json.load(file)
        api.signature = data['signature']
    app.run(debug=True)
