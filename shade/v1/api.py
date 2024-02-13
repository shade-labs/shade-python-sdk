import requests
from typing import Any
from dataclasses import dataclass


@dataclass
class APIException(Exception):
    status_code: int
    error: str

    def __str__(self):
        return f'Exception with Shade: {self.status_code} - {self.error}'


def handle_server_errors(func: callable) -> callable:
    """
    A decorator that for any response code > 400, raise a python exception and print the error
    """
    def wrapper(*args, **kwargs):
        resp = func(*args, **kwargs)
        # resp.raise_for_status()
        if not resp.ok:
            raise APIException(status_code=resp.status_code, error=resp.json())
        return resp
    return wrapper


class API:
    __ip: str

    def __init__(self, ip_: str):
        self.__ip = ip_

    @handle_server_errors
    def get(self, route: str, params: dict = None) -> Any:
        return requests.get(self.__ip + '/' + route, params=params)

    @handle_server_errors
    def put(self, route: str, params: dict = None, json: dict = None) -> Any:
        return requests.put(self.__ip + '/' + route, json=json, params=params)

    @handle_server_errors
    def post(self, route: str, params: dict = None, json: dict = None) -> Any:
        return requests.post(self.__ip + '/' + route, json=json, params=params)

    @handle_server_errors
    def delete(self, route: str, params: dict = None) -> Any:
        return requests.delete(self.__ip + '/' + route, params=params)
