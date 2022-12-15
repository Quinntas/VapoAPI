import json
import os
import subprocess
import time

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi.responses import FileResponse

from src.python.services.response import json_response

store = APIRouter()
last_refresh = time.time()
first_refresh = True


def check_last_refresh(current_time: float):
    seconds = 60
    minutes = 20
    return time.time() - current_time >= seconds * minutes


@store.get("/refresh")
async def refresh():
    global last_refresh
    global first_refresh

    if check_last_refresh(last_refresh) or first_refresh:
        first_refresh = False
        last_refresh = time.time()
        subprocess.Popen("python src/python/api/refresh.py", stdout=subprocess.PIPE, shell=False)
    return json_response(
        {
            "last_refresh": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(last_refresh)),
            "next_available_refresh": time.strftime('%Y-%m-%d %H:%M:%S',
                                                    time.localtime(last_refresh + 60 * 20))
        }
    )


@store.get("/products")
async def products():
    with open("data/products-vapo.json", "r") as file:
        return json_response(json.load(file))


@store.get("/featured")
async def featured():
    with open("data/products-vapo.json", "r") as file:
        return json_response(json.load(file)[:5])


@store.get("/categories")
async def categories():
    with open("data/categories-vapo.json", "r") as file:
        return json_response(json.load(file))


@store.get("/categories/images")
async def categories_images(slug: str):
    if os.path.exists(f'data/images/categories/{slug}.png'):
        return FileResponse(f"data/images/categories/{slug}.png")
    return HTTPException(404)
