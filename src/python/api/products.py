import asyncio
import html
import json
import re

import requests
from decouple import config

session = requests.session()
ACCESS_TOKEN = config('ACCESS_TOKEN')
REFRESH_TOKEN = config('REFRESH_TOKEN')
CLIENT_SECRET = config('CLIENT_SECRET')
CLIENT_ID = config('CLIENT_ID')
data = []
length = len(session.get(f"https://api.tagplus.com.br/produtos?access_token={ACCESS_TOKEN}").json())

with open('data/categories-vapo.json', 'r', encoding='utf-8') as f:
    categories = json.load(f)


def format_description(text: str):
    text = html.unescape(text).replace(u'\xa0', u' ').replace('"', '').replace("N'", '').replace('\n', '').replace('\t',
                                                                                                                   '')
    text = text.split(" ")
    text = ' '.join(text)
    return text


def check_category(c_id):
    for item in categories:
        if len(item['children']) >= 1:
            for child in item['children']:
                if child['id'] == c_id:
                    return {
                        "id": item['id'],
                        "name": item['name'],
                        "sub_category_id": child['id'],
                        "sub_category_name": child['name']
                    }


def adjust_price(price, sale):
    if sale == 0:
        return price
    return sale


async def add_product(x: int):
    res = session.get(f"https://api.tagplus.com.br/produtos/{x}?access_token={ACCESS_TOKEN}")
    parsed = res.json()
    gallery = parsed['imagens']
    if parsed['imagem_principal']['url'] in gallery:
        gallery.remove(parsed['imagem_principal']['url'])

    product = {
        "id": parsed['id'],
        "code": parsed['codigo'],
        "name": parsed['descricao'],
        "description": format_description(re.sub("\(.*?\)|\<.*?\>", "", parsed['descricao_longa'])),
        "slug": parsed['descricao'],
        "quantity": parsed['estoque']['qtd_revenda'],
        "category": check_category(parsed['categoria']['id']),
        "price": parsed['valor_venda_varejo'],
        "sale_price": adjust_price(parsed['valor_venda_varejo'], parsed['valor_oferta']),
        "image": parsed['imagem_principal']['url'],
        "gallery": gallery,
        "created_on": parsed['data_criacao']
    }
    data.append(product)


async def main():
    for x in range(1, length + 1):
        asyncio.create_task(add_product(x))


if __name__ == '__main__':
    asyncio.run(main())
    with open('data/products-vapo.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False))
