import json
import subprocess
import time

from fastapi import APIRouter

from src.python.services.response import json_response

store = APIRouter()
refreshing = False
last_refresh = time.time()


def check_last_refresh(current_time: float):
    seconds = 60
    minutes = 20
    return time.time() - current_time >= seconds * minutes


@store.get("/refresh")
async def refresh():
    global refreshing
    if check_last_refresh(last_refresh):
        refreshing = False
    if refreshing is False:
        refreshing = True
        subprocess.Popen("python src/python/api/refresh.py", stdout=subprocess.PIPE, shell=False)
    return json_response(
        {
            "last_refresh": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(last_refresh)),
            "next_available_refresh": time.strftime('%Y-%m-%d %H:%M:%S',
                                                    time.localtime(last_refresh + time.time() + 60 * 20))
        }
    )


@store.get("/products")
async def products():
    with open("data/products-vapo.json", "r") as file:
        return json_response(json.load(file))


@store.get("/categories")
async def categories():
    with open("data/categories-vapo.json", "r") as file:
        return json_response(json.load(file))
