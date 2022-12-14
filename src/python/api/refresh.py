import os

import requests
from decouple import config

ACCESS_TOKEN = config('ACCESS_TOKEN')
REFRESH_TOKEN = config('REFRESH_TOKEN')
CLIENT_SECRET = config('CLIENT_SECRET')
CLIENT_ID = config('CLIENT_ID')


def refresh_token():
    if requests.get(f"https://api.tagplus.com.br/produtos?access_token={ACCESS_TOKEN}").status_code == 401:
        res = requests.post('https://api.tagplus.com.br/oauth2/token',
                            data={
                                'grant_type': 'refresh_token',
                                'refresh_token': REFRESH_TOKEN,
                                'client_secret': CLIENT_SECRET,
                                'client_id': CLIENT_ID
                            })
        print(res.json())
        print(res.status_code)
        if res.status_code in range(1, 299):
            res = res.json()
            os.environ['REFRESH_TOKEN'] = res['refresh_token']
            os.environ['ACCESS_TOKEN'] = res['access_token']
        else:
            print("FAILED AT REFRESH TOKEN")


refresh_token()
os.system("python src/python/api/categories.py")
os.system("python src/python/api/products.py")
