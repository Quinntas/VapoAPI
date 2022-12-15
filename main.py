import socket
import time

import uvicorn
from decouple import config
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, FileResponse

from src.python.routers.v1.store import store
from src.python.services.response import json_response

API_STATE = config("API_STATE")

app = FastAPI(
    title="Vapo Vapo Store API",
    description="Vapo Vapo Store - Luna Cloud API",
    version="1.0",
    contact={
        "name": "Caio Quintas",
        "email": "caioquintassantiago@gmail.com",
    },
    license_info={
        "name": "MIT",
    },
    terms_of_service="MIT"
)


@app.get('/')
async def about():
    return json_response({
        "title": app.title,
        "description": app.description,
        "contact": app.contact,
        "license": app.license_info,
        "terms_of_service": app.terms_of_service
    })


@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse('static/icon.ico')


@app.exception_handler(404)
def item_not_found(request: Request, exception: HTTPException) -> JSONResponse:
    return json_response({"error": "Item Not Found"}, status_code=404)


@app.exception_handler(401)
def unauthorized(request: Request, exception: HTTPException) -> JSONResponse:
    return json_response({"error": "Unauthorized", "details": exception.detail}, status_code=401)


@app.exception_handler(400)
def bad_request(request: Request, exception: HTTPException) -> JSONResponse:
    return json_response({"error": "Bad Request", "details": exception.detail}, status_code=400)


@app.exception_handler(405)
def method_not_allowed(request: Request, exception: HTTPException) -> JSONResponse:
    return json_response({"error": "Method Not Allowed"}, status_code=405)


@app.exception_handler(500)
async def internal_server_error(request: Request, exception: HTTPException) -> JSONResponse:
    return json_response({"error": "Internal Server Error"}, status_code=500)


@app.exception_handler(403)
def forbidden(request: Request, exception: HTTPException) -> JSONResponse:
    return json_response({"error": "Forbidden", "details": exception.detail}, status_code=403)


@app.exception_handler(RequestValidationError)
async def validation_error(request: Request, exception: HTTPException) -> JSONResponse:
    return json_response(
        {"error": "Validation Error", "details": exception.__str__().replace('  ', '').replace('\n', ' | ')},
        status_code=422)


# Middleware
@app.middleware("http")
async def add_process_time(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


app.include_router(
    store,
    prefix="/api/v1/store",
    tags=["store"]
)


def main():
    host = socket.gethostbyname(socket.gethostname())
    port = 5000

    uvicorn.run("main:app", host=host, port=port, server_header=False)


if __name__ == "__main__" and API_STATE == 'Development':
    main()
