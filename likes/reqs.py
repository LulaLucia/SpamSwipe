'''Simple example of the Python requests module interacting with a web
application that supports REST

'''

import os
import requests

port = os.getuid()
base = f'http://localhost:{port}'

resp = requests.get(f'{base}/likes/apple')
print('GET /likes/apple =>', resp.json())

resp = requests.post(f'{base}/likes/apple')
print('POST /likes/apple =>', resp.json())

resp = requests.put(f'{base}/likes/apple', data={'set_likes': 200})
print('PUT /like/apple =>', resp.json())

resp = requests.get(f'{base}/likes/apple')
print('GET /likes/apple =>', resp.json())

