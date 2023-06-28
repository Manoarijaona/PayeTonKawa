import os
from datetime import datetime
from uuid import UUID

import requests
import json
import base64

from dotenv import load_dotenv

from dto.product_dto import ProductDTO

load_dotenv()
API_URL = os.getenv('API_URL')


def get_token_from_api_with_qrcode(passphrase: str):
    url = f'{API_URL}/users/login-qrcode'
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
    url = f'{API_URL}/products'
    headers = {'Content-Type': 'application/json'}
    response = requests.get(url, headers=headers)

    products_dto = []

    for product in response.json():
        product_dto = ProductDTO(
            id=UUID(product['id']),
            name=product['name'],
            description=product['description'],
            price=product['price'],
            stock=product['stock'],
            createdAt=datetime.strptime(product['createdAt'], '%Y-%m-%dT%H:%M:%S.%fZ'),
            updatedAt=datetime.strptime(product['updatedAt'], '%Y-%m-%dT%H:%M:%S.%fZ'),
            photo=product['photo']
        )
        products_dto.append(product_dto)

    return products_dto


get_all_product()
