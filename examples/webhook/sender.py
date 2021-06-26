# Twitcaspy
# Copyright 2021 Alma-field
# See LICENSE for details.

import requests
import json

def main():
    cassettes_file = '../../cassettes/testincomingwebhook.json'
    with open(cassettes_file, "r", encoding='utf-8')as file:
        data = json.load(file)
    response = requests.post(
        'http://localhost:5000/',
        data=json.dumps(data),
        headers={'Content-Type': 'application/json'})
    print(response.status_code)

if __name__ == '__main__':
    main()
