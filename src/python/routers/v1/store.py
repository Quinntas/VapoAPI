import asyncio
import json
import time

from fastapi import APIRouter

from src.python.api.refresh import run
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
        asyncio.create_task(run())
    return json_response({"refreshing": refreshing})


@store.get("/products")
async def products():
    with open("data/products-vapo.json", "r") as file:
        return json_response(json.load(file))


@store.get("/categories")
async def categories():
    with open("data/categories-vapo.json", "r") as file:
        return json_response(json.load(file))
