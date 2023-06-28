import requests
import json
import base64


def get_token_from_api_with_passphrase(passphrase: str):
    url = 'http://54.38.241.241:9090/users/login-qrcode'
    payload = {
        'passphrase': passphrase
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(payload), headers=headers)

    if response.status_code == 201 or response.status_code == 200:
        return response.json().get('token')
    else:
        return False


def token_decode(token: str):
    header, payload, signature = token.split('.')
    payload += '=' * (-len(payload) % 4)
    payload_bytes = base64.b64decode(payload)
    payload = payload_bytes.decode('utf-8')

    payload_data = json.loads(payload)

    print(payload_data)


def get_all_product():
    url = 'http://54.38.241.241:9090/products'
    headers = {'Content-Type': 'application/json'}
    response = requests.get(url, headers=headers)
    for product in response.json():
        print(product)


get_all_product()
