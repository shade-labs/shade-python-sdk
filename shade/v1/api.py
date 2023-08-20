import requests
from typing import Any


class API:
    __ip: str

    def __init__(self, ip_: str):
        self.__ip = ip_

    def get(self, route: str, params: dict = None) -> Any:
        return requests.get(self.__ip + '/' + route, params=params)

    def post(self, route: str, params: dict = None, data: dict = None) -> Any:
        return requests.post(self.__ip + '/' + route, data=data, params=params)
