import json

import requests
from decouple import config

ACCESS_TOKEN = config('ACCESS_TOKEN')
BASE_URL = config('BASE_URL')

url_categories = f'https://api.tagplus.com.br/categorias?access_token={ACCESS_TOKEN}'
url_products = f'https://api.tagplus.com.br/produtos?access_token={ACCESS_TOKEN}&categoria='

session = requests.session()
data = requests.get(url_categories).json()
parsedData = []

for item in data:
    if not item['categoria_mae']:
        parsedData.append(
            {
                'id': item['id'],
                'name': item['descricao'],
                'slug': item['descricao'],
                'productCount': len(session.get(f'{url_products}{item["id"]}').json()),
                'children': [],
                "icon": '',
                'image': {
                    'thumbnail': f'{BASE_URL}/api/v1/store/categories/images?slug={item["descricao"].lower()}',
                    'original': f'{BASE_URL}/api/v1/store/categories/images?slug={item["descricao"].lower()}'
                }
            }
        )

for item in data:
    if item['categoria_mae']:
        for cate in parsedData:
            if cate['id'] == item['categoria_mae']['id']:
                cate['children'].append(
                    {
                        "id": item['id'],
                        "name": item['descricao'],
                        "slug": item['descricao']
                    }
                )
                continue

with open('static/categories-vapo.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(parsedData, ensure_ascii=False))
